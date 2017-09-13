from django.shortcuts import render, redirect
from django.views.decorators.csrf import ensure_csrf_cookie

from .models import Quiz, Question


def index(request):
    return render(request, 'index.html')

@ensure_csrf_cookie
def quiz(request):
    questions = Quiz.create_random_questions()
    return render(request, 'quiz.html', {'questions': questions})

def results(request):
    questions = Answer.objects.question.all()
    guesses = Answer.objects.guess.all()
