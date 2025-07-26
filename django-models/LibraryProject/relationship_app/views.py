from django.shortcuts import render
from .models import Book

# Create your views here.
def listbooks(request):
    book_list = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': book_list} )