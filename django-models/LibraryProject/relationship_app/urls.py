from django.urls import path
from .views import list_books, LibraryDetailsView


urlpatterns = [
    path('books', list_books, name="list_of_books"),
    path('library', LibraryDetailsView.as_view(), name='library'  )
]