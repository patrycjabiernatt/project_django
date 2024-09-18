from django.contrib.auth.models import User
from django.contrib import admin
from wordmaster.models import Vocabulary


class WordmasterAdmin(admin.ModelAdmin):
    list_filter = ('level', 'categories')
    list_display = ('categories', 'english_word', 'polish_word')

admin.site.register(Vocabulary, WordmasterAdmin)


`