# bookshelf/forms.py

from django import forms

class ExampleForm(forms.Form):
    title = forms.CharField(label='Book Title', max_length=100)
    author = forms.CharField(label='Author Name', max_length=100)
    published_date = forms.DateField(label='Published Date', widget=forms.DateInput(attrs={'type': 'date'}))
