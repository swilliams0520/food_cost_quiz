import json
from pprint import pprint

from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils.six import BytesIO
from rest_framework.parsers import JSONParser
from django.http import HttpResponse

from game.models import Quiz
from .serializers import NewQuizSerializer, QuizSerializer, QuestionSerializer


class QuizAPIView(APIView):

    def get(self, request, format=None):
        quiz_json = NewQuizSerializer({'questions': Quiz.create_random_questions()})
        return Response(quiz_json.data)


def submit_quiz(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)

        total_score = 0

        for question in json_data['questions']:
            # question = QuestionSerializer(question)
            correct_answer = float(question['rounded_amount']) * float(question['variant']['avg_retail_price'])
            guess = float(question['guess']['amount'])
            guess_difference = abs(correct_answer - guess)

            if guess_difference <= 1:
                score = 10
            elif guess_difference > 1 and guess_difference <= 2:
                score = 5
            else:
                score = 0

            total_score += score

            pprint(total_score)




        return HttpResponse('')
