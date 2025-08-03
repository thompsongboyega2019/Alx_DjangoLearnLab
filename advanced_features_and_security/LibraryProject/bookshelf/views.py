# bookshelf/views.py
from django.shortcuts import render
from .models import Book
from django.db.models import Q
from django import forms

# Use a form to validate inputs
class SearchForm(forms.Form):
    query = forms.CharField(required=True, max_length=100)

def book_search(request):
    form = SearchForm(request.GET)
    books = []
    if form.is_valid():
        query = form.cleaned_data['query']
        books = Book.objects.filter(Q(title__icontains=query) | Q(author__icontains=query))
    return render(request, 'bookshelf/book_list.html', {'books': books, 'form': form})
