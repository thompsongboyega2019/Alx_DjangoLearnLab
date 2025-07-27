from django.shortcuts import render
from django.views.generic.detail import DetailView
from .models import Library, Book

# Create your views here.
def list_books(request):
    book_list = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': book_list} )



class LibraryDetailsView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'