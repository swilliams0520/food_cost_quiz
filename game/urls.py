from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^cost-quiz$', views.quiz, name='cost-quiz'),
    url(r'^one-pound-quiz$', views.one_pound_quiz, name='one-pound-quiz'),
    url(r'^results/(?P<quiz_id>[0-9]+)', views.results, name='results'),
]
