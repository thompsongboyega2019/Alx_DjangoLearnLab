# bookshelf/views.py

from django.shortcuts import render, redirect
from .forms import ExampleForm
from .models import Book

def book_create(request):
    if request.method == 'POST':
        form = ExampleForm(request.POST)
        if form.is_valid():
            Book.objects.create(
                title=form.cleaned_data['title'],
                author=form.cleaned_data['author'],
                published_date=form.cleaned_data['published_date']
            )
            return redirect('book_list')
    else:
        form = ExampleForm()

    return render(request, 'bookshelf/book_form.html', {'form': form})
