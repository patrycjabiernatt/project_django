from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import User
import csv
# Create your models here.


class Vocabulary(models.Model):
        categories = models.CharField(max_length=30, validators=[MinLengthValidator(3)])
        english_word = models.CharField(max_length=30, validators=[MinLengthValidator(3)], unique=True)
        polish_word = models.CharField(max_length=30, validators=[MinLengthValidator(3)])
        english_sentence = models.CharField(max_length=255, validators=[MinLengthValidator(10)])
        polish_sentence = models.CharField(max_length=255, validators=[MinLengthValidator(10)])
        level = models.CharField(max_length=2, validators=[MinLengthValidator(2)])



        def __str__(self):
                return f'{self.english_word}'


class Review(models.Model):
        user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
        vocabulary = models.ForeignKey(Vocabulary, on_delete=models.CASCADE, related_name='reviews')
        review_date = models.DateTimeField(auto_now_add=True)
        success = models.BooleanField(default=False)


class Quiz(models.Model):
        sentences = models.ForeignKey(Vocabulary, on_delete=models.CASCADE, related_name='quiz')
        quiz_date = models.DateTimeField(auto_now_add=True)
        success = models.BooleanField(default=False)

