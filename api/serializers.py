from rest_framework import serializers

from game.models import Consumable, Variant, Question, Quiz, Guess

class ConsumableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consumable
        fields = '__all__'

class VariantSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    consumable = ConsumableSerializer()

    class Meta:
        model = Variant
        fields = ('id', 'storage_type', 'avg_retail_price',
                  'retail_price_measurement', 'prep_yield_factor',
                  'size_of_cup_equivalent', 'size_of_cup_eq_measurement',
                  'avg_price_per_cup', 'addendum', 'consumable')

class GuessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guess
        fields = ('amount',)

class QuestionSerializer(serializers.ModelSerializer):
    variant = VariantSerializer()
    guess = GuessSerializer()
    rounded_amount = serializers.DecimalField(max_digits=12, decimal_places=4)

    class Meta:
        model = Question
        fields = ('variant', 'guess', 'rounded_amount')

    def create(self, validated_data):
        question = Question()
        question.amount = validated_data['rounded_amount']
        variant = Variant.objects.get(id=validated_data['variant']['id'])
        question.variant = variant
        question.save()
        return question


class NewQuizSerializer(serializers.Serializer):
    questions = QuestionSerializer(many=True)

class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)
    class Meta:
        model = Quiz
        fields = '__all__'
