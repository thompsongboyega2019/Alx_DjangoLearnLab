from django.urls import path
from .views import list_books, LibraryDetailView, SignUpView
from django.contrib.auth.views import LoginView, LogoutView



urlpatterns = [
    path('books', list_books, name="list_of_books"),
    path('register', SignUpView.as_view(), name='register'),
    path('library', LibraryDetailView.as_view(), name='library'  ),
    path('login', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('', LogoutView.as_view(), name='logout'),
    
]