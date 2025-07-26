from django.urls import path
from . import views


urlpatterns = [
    path('books', views.listbooks, name="list_of_books"),
]