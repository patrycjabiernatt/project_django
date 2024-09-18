from django import template
from django.utils.safestring import mark_safe
import re


register = template.Library()



@register.filter(name='replace_with_form')
def replace_with_form(sentence, word):
    word_lower = word.lower()


    form_html = f"""
    <form method="post" class="uk-inlin">
        <input type='hidden' name='page' value='{{{{ words.number }}}}'>
        <input class="uk-margin-small-left uk-margin-small-right" placeholder='Wpisz słówko' id='eng_word' name='eng_word'>
        <button type='submit' class='uk-margin-small uk-button uk-button-primary uk-border-rounded'>Sprawdź</button>
    </form>
    """

    def replace_case_insensitive(text, search, replace):
        escaped_search = ' '.join(re.escape(word) for word in search.split())
        pattern =  f'(?i)\\b{escaped_search}s?\\b'
        return re.sub(pattern, replace, text)

    replaced_sentence = replace_case_insensitive(sentence, word_lower, form_html)

    return mark_safe(replaced_sentence)


@register.filter(name='contains_word')
def contains_word(sentence, word):
    pattern = rf'\b{re.escape(word)}\b'

    return re.search(pattern, sentence, re.IGNORECASE) is not None