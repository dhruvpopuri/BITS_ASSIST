from django.shortcuts import render,redirect
from django.urls import reverse
from .models import Questions, Answers, Reports
from django.views.generic import ListView,CreateView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from users.models import Profile
from django.contrib.auth.models import User
from django.db.models import UniqueConstraint
from django.contrib import messages


# Create your views here.


@login_required
def dashboard(request):
	questions = Questions.objects.all()
	for question in questions:
		question.q_likes = question.q_likedby.count()
		question.save()

		if f'report{question.pk}' in request.POST:
			question.report.create(report_url=f'http://127.0.0.1:8000/answers/{question.pk}/')
			messages.add_message(request, messages.SUCCESS, 'Reported Successfully')
			




	questions3 = Questions.objects.order_by('-pub_time','-q_likes')
	context = {
	'questions3':questions3,

	}
	


	return render(request,'Dashboard/dashboard.html',context)



class QuestionCreateView(LoginRequiredMixin,CreateView):
	model = Questions
	fields = ['question_text']
	template_name='Dashboard/Ask_Q.html'

	def form_valid(self, form):
		form.instance.asked_by = self.request.user
		return super().form_valid(form)


@login_required
def answers(request,pk):
	question = Questions.objects.get(pk=pk)
	answers = question.answers.all()
	user = request.user
	liked_by = question.q_likedby
	ques_dislikedby = question.q_dislikedby
	if user in liked_by.all():
		liked = True
	else:
		liked = False

	if user in ques_dislikedby.all():
		disliked = True
	else:
		disliked = False

	#Question Like button
	if user in liked_by.all() or user in ques_dislikedby.all():
		if user in liked_by.all() and user not in ques_dislikedby.all():

			#unlike button
			if 'like' in request.POST:
				liked_by.remove(user)
				liked = False

			likes = liked_by.count()

		elif user in ques_dislikedby.all() and user not in liked_by.all():

			#unDislike button
			if 'dislike' in request.POST:
				ques_dislikedby.remove(user)
				disliked = False

			dislikes = ques_dislikedby.count()






	else:
		if 'like' in request.POST:
			liked_by.add(user)
			liked = True
		
		#Question Dislike button
		if 'dislike' in request.POST :
			ques_dislikedby.add(user)
			disliked = True


		
	
	likes = liked_by.count()
	ques_dislikes=ques_dislikedby.count()


		

	

	if f'report{pk}' in request.POST:
			question.report.create(report_url=f'http://127.0.0.1:8000/answers/{pk}/')
			messages.add_message(request, messages.SUCCESS, 'Reported Successfully')

		
		

	#answers_likebutton
	answers = question.answers.all()
	for answer in answers:
		ans_likedby = answer.answer_likedby
		ans_dislikedby = answer.answer_dislikedby

		if user in ans_likedby.all() or user in ans_dislikedby.all():
			if user in ans_likedby.all() and user not in ans_dislikedby.all():
				if f'Like{answer.pk}' in request.POST:   # ********************
					ans_likedby.remove(user)
					



			

			if user not in ans_likedby.all() and user in ans_dislikedby.all():
				if f'Dislike{answer.pk}' in request.POST:    #*****************
					ans_dislikedby.remove(user)
					



		else:
			if f'Like{answer.pk}' in request.POST:
				ans_likedby.add(user)
				


			if f'Dislike{answer.pk}' in request.POST:
				ans_dislikedby.add(user)

		answer.answer_likes = ans_likedby.count()
		answer.save()

	answers = question.answers.order_by('-answer_likes')
	author = question.asked_by





	context = {
	'question':question,
	'answers':answers,
	'likes':likes,
	'ques_dislikes':ques_dislikes,
	'author':author,
	'user':user,
	'liked':liked,
	'disliked':disliked,

	}
		
		


	return render(request,'Dashboard/answers.html',context)

class AnswerCreateView(LoginRequiredMixin,CreateView):
	model = Answers
	fields = ['answer']
	template_name = 'Dashboard/submit-ans.html'

	def form_valid(self, form,**kwargs):
		form.instance.answer_l = Questions.objects.get(pk=self.kwargs["pk"])
		form.instance.answered_by = self.request.user
		return super().form_valid(form)


class QuestionUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
	model = Questions
	fields = ['question_text']
	template_name = 'Dashboard/question_update.html'


	def form_valid(self, form):
		form.instance.asked_by = self.request.user
		return super().form_valid(form)

	def test_func(self,**kwargs):
		post = Questions.objects.get(pk=self.kwargs["pk"])
		if post.asked_by == self.request.user:
			return True
		return False

class QuestionDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
	model = Questions
	template_name = 'Dashboard/question_delete.html'

	def test_func(self,**kwargs):
		post = Questions.objects.get(pk=self.kwargs["pk"])
		if post.asked_by == self.request.user:
			return True
		return False

	def get_success_url(self):
		return reverse('dashboard')

class AnswerUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
	model = Answers
	fields = ['answer']
	template_name = 'Dashboard/ans-update.html'

	def test_func(self,**kwargs):
		answer = Answers.objects.get(pk=self.kwargs['pk'])
		if answer.answered_by == self.request.user:
			return True
		return False


class AnswerDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
	model = Answers
	template_name = 'Dashboard/Ans-delete.html'

	def test_func(self,**kwargs):
		answer = Answers.objects.get(pk=self.kwargs['pk'])
		if answer.answered_by == self.request.user:
			return True
		return False

	def get_success_url(self):
		return reverse('dashboard')




















