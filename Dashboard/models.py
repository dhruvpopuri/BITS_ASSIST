from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from django.db.models import UniqueConstraint


# Create your models here.

class Questions(models.Model):
	question_text = models.CharField(max_length=300)
	asked_by = models.ForeignKey(User,on_delete=models.CASCADE)
	pub_time = models.DateTimeField(default=timezone.now)
	q_likedby = models.ManyToManyField(User,related_name='liked_by')
	q_dislikedby = models.ManyToManyField(User,related_name='disliked_by')
	q_likes = models.IntegerField(default=0)


	def __str__(self):
		return self.question_text

	def get_absolute_url(self):
		return reverse('dashboard')


class Answers(models.Model):
	answer_l = models.ForeignKey(Questions, on_delete=models.CASCADE,null=True,related_name='answers')
	answer = models.TextField()
	answered_by = models.ForeignKey(User, on_delete=models.CASCADE)
	answer_time = models.DateTimeField(default=timezone.now)
	answer_likedby = models.ManyToManyField(User,related_name='ansliked_by')
	answer_dislikedby = models.ManyToManyField(User,related_name='ansdisliked_by')
	answer_likes = models.IntegerField(default=0)


	def __str__(self):
		return self.answer

	def get_absolute_url(self):
		return reverse('dashboard')



class Reports(models.Model):
	report_ques = models.ForeignKey(Questions,on_delete=models.CASCADE,null=True,related_name='report')
	report_url = models.URLField()
	









