from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^cost-quiz$', views.CostQuizAPIView.as_view(), name="cost-quiz"),
    url(r'^pound-quiz$', views.PoundQuizAPIView.as_view(), name="pound-quiz"),
    url(r'^quiz-submit$', views.submit_quiz, name="submit-quiz"),
]
