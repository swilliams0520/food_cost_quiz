import random
import re

from django.db import models


class Consumable(models.Model):
    name = models.CharField(max_length=128)
    sources = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.name}'

class Variant(models.Model):
    storage_type = models.CharField(max_length=128)
    avg_retail_price = models.DecimalField(max_digits=12, decimal_places=8)
    retail_price_measurement = models.CharField(max_length=128)
    prep_yield_factor = models.DecimalField(max_digits=12, decimal_places=8)
    size_of_cup_equivalent = models.DecimalField(max_digits=12, decimal_places=8)
    size_of_cup_eq_measurement = models.CharField(max_length=128)
    avg_price_per_cup = models.DecimalField(max_digits=12, decimal_places=8)
    addendum = models.TextField(blank=True, null=True)

    consumable = models.ForeignKey(Consumable, related_name='variants', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.consumable}: {self.storage_type}'

class Question(models.Model):
    variant = models.ForeignKey(Variant)
    amount = models.DecimalField(max_digits=12, decimal_places=4)

    @property
    def rounded_amount(self):
        return round(self.amount * 4) / 4

    @property
    def actual_price(self):
        return self.amount * self.variant.avg_retail_price

    @property
    def singular_measurement(self):
        if re.search(r'.+s$', self.variant.size_of_cup_eq_measurement) and self.amount == 1:
            return self.variant.size_of_cup_eq_measurement[:-1]
        else:
            return self.variant.size_of_cup_eq_measurement

    def __str__(self):
        return f'How much does {self.rounded_amount} {self.variant.size_of_cup_eq_measurement} of {self.variant.storage_type} {self.variant.consumable.name} cost?'

#return f'How much of a {self.variant.storage_type} is edible?

class Guess(models.Model):
    question = models.OneToOneField(Question)
    amount = models.DecimalField(max_digits=12, decimal_places=4)

    class Meta:
        verbose_name_plural = 'guesses'


class Quiz(models.Model):
    questions = models.ManyToManyField(Question, through='Answer', through_fields=('quiz', 'question'))

    @staticmethod
    def create_questions(is_random=True, default=1, amount=10):
        previous_question_ids = list()
        questions = list()

        for _ in range(amount):
            question = Question()
            unique = False

            while not unique:
                variants = Variant.objects.values_list('id', flat=True)
                variant_id = random.choice(variants)
                question.variant = Variant.objects.get(id=variant_id)

                if (question.variant.id, question.variant.consumable.id) not in previous_question_ids:
                    unique = True
                if len(variants) <= len(previous_question_ids):
                    break

            if is_random == True:
                question.amount = (random.random() * 4) + 0.5
            else:
                question.amount = default

            if unique:
                previous_question_ids.append((question.variant.id, question.variant.consumable.id))
                questions.append(question)

        return questions


    def get_results(self):
        total_score = 0
        for answer in self.answer_set.all():
            answer_difference = answer.guess_difference

            if answer_difference <= 1:
                score = 10
            elif answer_difference > 1 and answer_difference <= 2:
                score = 5
            else:
                score = 0

            total_score += score

        return total_score

    class Meta:
        verbose_name_plural = 'quizzes'

class Answer(models.Model):
    guess = models.ForeignKey(Guess)
    question = models.ForeignKey(Question)
    quiz = models.ForeignKey(Quiz)

    @property
    def guess_difference(self):
        return abs(self.guess.amount - (self.question.amount * self.question.variant.avg_retail_price))
