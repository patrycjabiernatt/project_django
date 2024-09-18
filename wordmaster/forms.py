from django import forms

class SentenceForm(forms.Form):
    input_field = forms.CharField(label='', max_length=25)