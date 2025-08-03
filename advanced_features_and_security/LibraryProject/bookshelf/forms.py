# bookshelf/forms.py

from django import forms

class SearchForm(forms.Form):
    query = forms.CharField(required=True, max_length=100)
