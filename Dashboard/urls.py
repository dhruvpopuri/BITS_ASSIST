from django.urls import path
from .views import (QuestionCreateView,
	AnswerCreateView,
	QuestionUpdateView,
	QuestionDeleteView,
	AnswerUpdateView,
	AnswerDeleteView)
from . import views
from .models import Questions

urlpatterns = [
	path('',views.dashboard,name='dashboard'),
	path('Ask/',QuestionCreateView.as_view(),name='ask'),
	path('answers/<int:pk>/',views.answers,name='answers'),
	path('answers/<int:pk>/submit_ans',AnswerCreateView.as_view(),name='submit_ans'),
	path('answers/<int:pk>/update/',QuestionUpdateView.as_view(),name='update'),
	path('answers/<int:pk>/delete/',QuestionDeleteView.as_view(),name='delete'),
	path('answers/update/<int:pk>/',AnswerUpdateView.as_view(),name='ans-update'),
	path('answers/delete/<int:pk>',AnswerDeleteView.as_view(),name='ans-delete')



	



]