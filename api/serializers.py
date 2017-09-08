from rest_framework import serializers

from game.models import Consumable, Variant, Question, Quiz, Guess

class ConsumableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consumable
        fields = '__all__'

class VariantSerializer(serializers.ModelSerializer):
    consumable = ConsumableSerializer()

    class Meta:
        model = Variant
        fields = '__all__'

class GuessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guess
        fields = ('amount',)

class QuestionSerializer(serializers.ModelSerializer):
    variant = VariantSerializer()
    guess = GuessSerializer()

    class Meta:
        model = Question
        fields = ('variant', 'guess', 'rounded_amount')

class NewQuizSerializer(serializers.Serializer):
    questions = QuestionSerializer(many=True)
