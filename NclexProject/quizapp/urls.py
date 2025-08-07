
from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('register',views.register,name='register'),
    path('login',views.login_view,name='login'),
    path('logout',views.logout_view,name='logout'),
    path('topic',views.topic_view,name='topic'),
    path('startquiz/<int:topic_id>',views.start_quiz_view,name='start_quiz'),
    path('question',views.question_view,name='question_view'),
    path('result',views.result_view,name='result_view'),
    path('review/<int:topic_id>',views.review_mistakes,name='review'),
]
