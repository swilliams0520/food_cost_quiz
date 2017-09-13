from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^cost-quiz$', views.QuizAPIView.as_view(), name="cost-quiz"),
    url(r'^cost-quiz-submit$', views.submit_quiz, name="submit-quiz"),
]
