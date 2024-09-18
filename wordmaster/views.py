from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from . models import Vocabulary, Review
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.utils.html import format_html
from .forms import SentenceForm
import re
from users.models import Score
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.models import User
import random


# Create your views here.
@login_required
def view_first(request):
    context = {
        'title_app': 'WordMaster'
    }
    return render(request, 'wordmaster/main_view.html', context)

@login_required
def choice_category(request):
    unique_categories = list(Vocabulary.objects.values_list('categories', flat=True).distinct())
    context = {

        'cat': unique_categories,
        'title_app': 'WordMaster'
    }
    return render(request, 'wordmaster/categories.html', context)

@login_required
def words_by_category_view(request, category_name):
    filtered_words = Vocabulary.objects.filter(categories=category_name, )
    levels = Vocabulary.objects.filter(categories=category_name).values_list('level', flat=True).distinct().order_by('level')


    context = {
        'category_name': category_name,
        'levels': levels,
        'title_app': 'WordMaster'
    }

    return render(request, 'wordmaster/cat-lev.html', context)
@login_required
def words_by_category_level_view(request, category_name, level):
    filtered_words = Vocabulary.objects.filter(categories=category_name, level=level)

    levels = Vocabulary.objects.filter(categories=category_name).values_list('level', flat=True).distinct()


    paginator = Paginator(filtered_words, 1)
    page = request.GET.get('page')

    try:
        words = paginator.page(page)
    except PageNotAnInteger:
        words = paginator.page(1)
    except EmptyPage:
        words = paginator.page(paginator.num_pages)



    context = {
        'words': words,
        'category_name': category_name,
        'level': level,
        'filtered_words': filtered_words,
        'title_app': 'WordMaster'
    }

    return render(request, 'wordmaster/worddd.html', context)

@login_required
def add_to_review(request, word_id):
    word = get_object_or_404(Vocabulary, id=word_id)

    word_review, created = Review.objects.get_or_create(vocabulary=word, user=request.user,)



    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def review_words_view(request):

    filtered_pog = Review.objects.filter(vocabulary__categories='Pogoda')
    filtered_healthy = Review.objects.filter(vocabulary__categories='Zdrowie')
    filtered_technology = Review.objects.filter(vocabulary__categories='Technologia')
    filtered_travel = Review.objects.filter(vocabulary__categories='Podróże')
    filtered_climate = Review.objects.filter(vocabulary__categories='Klimat')
    filtered_psychology = Review.objects.filter(vocabulary__categories='Psychologia')
    filtered_B1 = Review.objects.filter(vocabulary__level='B1')
    filtered_B2 = Review.objects.filter(vocabulary__level='B2')
    filtered_C1 = Review.objects.filter(vocabulary__level='C1')



    context = {
    'filtered_pog' : filtered_pog,
    'filtered_healthy' : filtered_healthy,
    'filtered_technology' : filtered_technology,
    'filtered_travel' : filtered_travel,
    'filtered_climate' : filtered_climate,
    'filtered_psychology' : filtered_psychology,
    'filtered_B1' : filtered_B1,
    'filtered_B2' : filtered_B2,
    'filtered_C1' : filtered_C1,
    'title_app': 'WordMaster'
    }

    return render(request, 'wordmaster/abb.html', context)

@login_required
def review_by_cat(request, cat_name):
    filtered_pog = Review.objects.filter(vocabulary__categories=cat_name, user=request.user)

    paginator = Paginator(filtered_pog, 1)
    page = request.GET.get('page')

    try:
        words = paginator.page(page)
    except PageNotAnInteger:
        words = paginator.page(1)
    except EmptyPage:
        words = paginator.page(paginator.num_pages)

    context = {
        'cat_name': cat_name,
        'words': words,
        'title_app': 'WordMaster'

    }

    return render(request, 'wordmaster/word_reviews.html', context)


@login_required
def review_by_level(request, level):
    filtered_B1 = Review.objects.filter(vocabulary__level=level, user=request.user)

    # Paginacja
    paginator = Paginator(filtered_B1, 1)
    page = request.GET.get('page')

    try:
        words = paginator.page(page)
    except PageNotAnInteger:
        words = paginator.page(1)
    except EmptyPage:
        words = paginator.page(paginator.num_pages)

    context = {
        'level': level,
        'words': words,
        'title_app': 'WordMaster'
    }

    return render(request, 'wordmaster/word_reviews_by_level.html', context)

@login_required
def delete_from_review(request, word_id):

    word = Review.objects.get(id=word_id)

    # Dodaj słówko do powtórek
    word.delete()

    return redirect(request.META.get('HTTP_REFERER', '/'))

def take_quiz_cat(request, category_name):
    filtered_sentence = Vocabulary.objects.filter(categories=category_name, )
    levels = filtered_sentence.values_list('level', flat=True).distinct().order_by(
        'level')

    context = {
        'category_name': category_name,
        'levels': levels,

    }

    return render(request, 'wordmaster/quiz_cat.html', context)
    
    

@login_required
def quiz_filter_view(request):

    filtered_pog = Review.objects.filter(vocabulary__categories='Pogoda')
    filtered_healthy = Review.objects.filter(vocabulary__categories='Zdrowie')
    filtered_technology = Review.objects.filter(vocabulary__categories='Technologia')
    filtered_travel = Review.objects.filter(vocabulary__categories='Podróże')
    filtered_climate = Review.objects.filter(vocabulary__categories='Klimat')
    filtered_psychology = Review.objects.filter(vocabulary__categories='Psychologia')
    filtered_B1 = Review.objects.filter(vocabulary__level='B1')
    filtered_B2 = Review.objects.filter(vocabulary__level='B2')
    filtered_C1 = Review.objects.filter(vocabulary__level='C1')



    context = {
    'filtered_pog' : filtered_pog,
    'filtered_healthy' : filtered_healthy,
    'filtered_technology' : filtered_technology,
    'filtered_travel' : filtered_travel,
    'filtered_climate' : filtered_climate,
    'filtered_psychology' : filtered_psychology,
    'filtered_B1' : filtered_B1,
    'filtered_B2' : filtered_B2,
    'filtered_C1' : filtered_C1,
    'title_app': 'WordMaster'
    }

    return render(request, 'wordmaster/filter_quiz.html', context)


@login_required
def sentence_quiz(request, category_name, level):

    filtered_sentence = Vocabulary.objects.filter(categories=category_name, level=level)


    # Paginacja
    paginator = Paginator(filtered_sentence, 1)
    page = request.GET.get('page')

    try:
        words = paginator.page(page)
    except PageNotAnInteger:
        words = paginator.page(1)
    except EmptyPage:
        words = paginator.page(paginator.num_pages)



    context = {
        'words': words,
        'category_name': category_name,
        'filtered_sentence': filtered_sentence,
        'title_app': 'WordMaster'
    }

    return render(request, 'wordmaster/quiz_sentence.html', context)


@login_required
@csrf_exempt
def quiz_level(request, lev):

    if 'selected_words' not in request.session:
        B1_word = Vocabulary.objects.filter(level=lev).order_by('english_sentence')
        filtered_words = [word for word in B1_word]
        selected_words = random.sample(filtered_words, min(10, len(filtered_words)))
        request.session['selected_words'] = [word.id for word in selected_words]
        request.session['quiz_points'] = 0
        request.session['current_question'] = 1
    else:
        selected_words = Vocabulary.objects.filter(id__in=request.session['selected_words'])

    paginator = Paginator(selected_words, 1)
    page = request.GET.get('page') or request.POST.get('page')

    try:
        words = paginator.page(page)
    except PageNotAnInteger:
        words = paginator.page(1)
    except EmptyPage:
        words = paginator.page(paginator.num_pages)

    if request.method == 'POST':
        user_input = request.POST.get('eng_word').strip().lower()
        current_word = words.object_list[0].english_word.lower()


        if user_input == current_word:
            request.session['quiz_points'] += 1
            messages.success(request, 'Gratulacje! Zdobyłeś punkt!')
        else:
            messages.error(request, 'Niestety, nie zdobyłeś punktu!')

        request.session['current_question'] += 1
        if words.has_next():
            return redirect('{}?page={}'.format(request.path, words.next_page_number()))
        else:
            Score.objects.create(user=request.user, points=request.session['quiz_points'])
            messages.success(request, f'Test zakończony! Zdobyłeś {request.session["quiz_points"]} punktów.')
            del request.session['selected_words']
            del request.session['quiz_points']
            del request.session['current_question']
            return redirect('view_first_url')



    csrf_token = get_token(request)

    context = {
        'lev': lev,
        'words': words,
        'csrf_token': csrf_token,
        'current_question': request.session.get('current_question', 1),
        'total_questions': len(request.session['selected_words']),
        'title_app': 'WordMaster'
    }

    return render(request, 'wordmaster/level_by_quiz.html', context)

@login_required
@csrf_exempt
def quiz_cat(request, category):

    if 'selected_words' not in request.session:
        technology_word = Vocabulary.objects.filter(categories=category).order_by('english_sentence')
        filtered_words = [word for word in technology_word]
        selected_words = random.sample(filtered_words, min(10, len(filtered_words)))
        request.session['selected_words'] = [word.id for word in selected_words]  # Zapisz ID wybranych słów
        request.session['quiz_points'] = 0
        request.session['current_question'] = 1
    else:
        selected_words = Vocabulary.objects.filter(id__in=request.session['selected_words'])

    paginator = Paginator(selected_words, 1)
    page = request.GET.get('page') or request.POST.get('page')

    try:
        words = paginator.page(page)
    except PageNotAnInteger:
        words = paginator.page(1)
    except EmptyPage:
        words = paginator.page(paginator.num_pages)

    if request.method == 'POST':
        user_input = request.POST.get('eng_word').strip().lower()
        current_word = words.object_list[0].english_word.lower()


        if user_input == current_word:
            request.session['quiz_points'] += 1
            messages.success(request, 'Gratulacje! Zdobyłeś punkt!')
        else:
            messages.error(request, 'Niestety, nie zdobyłeś punktu!')

        request.session['current_question'] += 1
        if words.has_next():
            return redirect('{}?page={}'.format(request.path, words.next_page_number()))
        else:
            Score.objects.create(user=request.user, points=request.session['quiz_points'])
            messages.success(request, f'Test zakończony! Zdobyłeś {request.session["quiz_points"]} punktów.')
            del request.session['selected_words']
            del request.session['quiz_points']
            del request.session['current_question']
            return redirect('view_first_url')

    csrf_token = get_token(request)

    context = {
        'category': category,
        'words': words,
        'csrf_token': csrf_token,
        'current_question': request.session.get('current_question', 1),
        'total_questions': len(request.session['selected_words']),
        'title_app': 'WordMaster'
    }

    return render(request, 'wordmaster/cat_quiz.html', context)

@login_required
def change_category(request, category):
    if 'selected_words' in request.session:
        del request.session['selected_words']
        del request.session['quiz_points']
        del request.session['current_question']

    return redirect(reverse('quiz_cat_url', kwargs={'category': category}))















