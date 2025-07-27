from django.urls import path
from . import views


urlpatterns = [
    path('books', views.listbooks, name="list_of_books"),
    path('library', views.LibraryDetailsView.as_view(), name='library'  )
]