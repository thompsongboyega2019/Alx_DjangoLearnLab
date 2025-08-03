# bookshelf/views.py

from django.shortcuts import render
from django.db.models import Q
from .models import Book
from .forms import SearchForm  # ✅ Correct import

def book_search(request):
    form = SearchForm(request.GET)
    books = []
    if form.is_valid():
        query = form.cleaned_data['query']
        books = Book.objects.filter(Q(title__icontains=query) | Q(author__icontains=query))
    return render(request, 'bookshelf/book_list.html', {'books': books, 'form': form})
