from django.urls import path
from . import views

urlpatterns = [

    path('categories', views.choice_category, name='choice_category_url'),
    path('', views.view_first, name='view_first_url'),
    path('categories/<str:category_name>/', views.words_by_category_view, name='view_words_by_category_url'),
    path('categories/<str:category_name>/<str:level>', views.words_by_category_level_view, name='view_words_by_category_level_url'),
    path('add-to-review/<int:word_id>/', views.add_to_review, name='add_to_review_url'),
    path('review-words-view/', views.review_words_view, name='review_words_view_url'),
    path('reviews/<str:cat_name>', views.review_by_cat, name='review_by_cat_url'),
    path('reviews/<str:level>/', views.review_by_level, name='review_by_level_url'),
    path('delete-from-review/<int:word_id>/', views.delete_from_review, name='delete_from_review_url'),
    path('quiz-filter-view/', views.quiz_filter_view, name='quiz_filter_view_url'),
    path('quiz/<str:category_name>/<str:level>/', views.sentence_quiz, name='sentence_quiz_url'),
    path('quiz/<str:lev>/', views.quiz_level, name='quiz_level_url'),
    path('quiz/<str:category>', views.quiz_cat, name='quiz_cat_url'),
    path('change-category/<str:category>/', views.change_category, name='change_category_url'),



]