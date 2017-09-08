from rest_framework.views import APIView
from rest_framework.response import Response

from game.models import Quiz
from .serializers import NewQuizSerializer


class QuizAPIView(APIView):
    def get(self, request, format=None):
        quiz_json = NewQuizSerializer({'questions': Quiz.create_random_questions()})
        return Response(quiz_json.data)
