from django.contrib import admin

from . import models

@admin.register(models.Consumable)
class ConsumableAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Variant)
class VariantAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Question)
class QuestionAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Guess)
class GuessAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Quiz)
class QuizAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Answer)
class AnswerAdmin(admin.ModelAdmin):
    pass
