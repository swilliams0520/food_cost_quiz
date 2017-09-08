from django.shortcuts import render, redirect

from .models import Quiz, Question


def index(request):
    return render(request, 'index.html')

def quiz(request):
    questions = Quiz.create_random_questions()
    return render(request, 'quiz.html', {'questions': questions})

def results(request):
    questions = Answer.objects.question.all()
    guesses = Answer.objects.guess.all()
