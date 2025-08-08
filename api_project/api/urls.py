from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import BookList


urlpatterns = [
    path('books/', BookList.as_view(), name='book-list'), 
]