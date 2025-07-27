from django.urls import path
from .views import list_books, LibraryDetailView


urlpatterns = [
    path('books', list_books, name="list_of_books"),
    path('library', LibraryDetailView.as_view(), name='library'  )
]