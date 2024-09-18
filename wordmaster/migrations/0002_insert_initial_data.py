from django.db import migrations
from wordmaster.models import Vocabulary

import datetime
import csv


def load_initial_data(apps, schema_editor):
    word_list = []
    with open ('wordmaster/migrations/datas.csv', 'r', encoding='utf-8') as word_file:
        reader = csv.DictReader(word_file, delimiter=',')

        for row in reader:
            word_list.append(Vocabulary(
            categories= row['categories'],
            english_word = row['english_word'],
            polish_word = row['polish_word'],
            english_sentence = row['english_sentence'],
            polish_sentence = row['polish_sentence'],
            level = row['level'],
            ))

    Vocabulary.objects.bulk_create(word_list)


class Migration(migrations.Migration):
    initial = False

    dependencies = [('wordmaster', '0001_initial'),


    ]

    operations = [
    migrations.RunPython(load_initial_data),
    ]