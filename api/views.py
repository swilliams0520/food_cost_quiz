import json
from pprint import pprint

from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils.six import BytesIO
from rest_framework.parsers import JSONParser
from django.http import HttpResponse
from django.db import transaction, IntegrityError

from game.models import Quiz, Guess, Answer
from .serializers import NewQuizSerializer, QuizSerializer, QuestionSerializer


class CostQuizAPIView(APIView):
    def get(self, request, format=None):
        quiz_json = NewQuizSerializer({'questions': Quiz.create_questions()})
        return Response(quiz_json.data)

class PoundQuizAPIView(APIView):
    def get(self, request, format=None):
        quiz_json = NewQuizSerializer({'questions': Quiz.create_questions(is_random=False)})
        return Response(quiz_json.data)

def submit_quiz(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)

        total_score = 0
        try:
            with transaction.atomic():
                quiz = Quiz.objects.create()
                for question_data in json_data['questions']:
                    question = QuestionSerializer(data=question_data)

                    if question.is_valid():
                        question = question.save()
                    else:
                        raise IntegrityError

                    guess_amount = float(question_data['guess']['amount'])
                    guess = Guess.objects.create(amount=guess_amount, question=question)
                    answer = Answer.objects.create(guess=guess, question=question, quiz=quiz)
                    quiz.answer_set.add(answer)

                quiz.save()
                return HttpResponse(quiz.id)

        except BaseException as e:
            raise e from None




        return HttpResponse('')
