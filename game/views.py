from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib import messages

from .models import Quiz, Question


def index(request):
    return render(request, 'index.html')

@ensure_csrf_cookie
def quiz(request):
    questions = Quiz.create_random_questions()
    return render(request, 'quiz.html', {'questions': questions})

def results(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    score = quiz.get_results()
    
    if score >= 50:
        messages.info(request, 'Great job, you recieved an exemplary score!')
    elif score >= 20 and score < 50:
        messages.info(request, 'Nice work, you did pretty well!')
    else:
        messages.info(request, 'Hit the grocery store and start taking notes - your food cost knowledge is weak.')
    return render(request, 'results.html', {'quiz': quiz, 'score': quiz.get_results()})
