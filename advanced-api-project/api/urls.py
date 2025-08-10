# api/urls.py

from django.urls import path, include
from . import views

urlpatterns = [
    # Book CRUD endpoints - ALX required format
    path('books/', views.BookListView.as_view(), name='book-list'),
    path('books/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),
    path('books/create/', views.BookCreateView.as_view(), name='book-create'),
    path('books/update/<int:pk>/', views.BookUpdateView.as_view(), name='book-update'),
    path('books/delete/<int:pk>/', views.BookDeleteView.as_view(), name='book-delete'),
    
    # Author CRUD endpoints
    path('authors/', views.AuthorListView.as_view(), name='author-list'),
    path('authors/<int:pk>/', views.AuthorDetailView.as_view(), name='author-detail'),
    path('authors/create/', views.AuthorCreateView.as_view(), name='author-create'),
    
    # Custom endpoints
    path('books/search/', views.book_search, name='book-search'),
    path('authors/stats/', views.author_statistics, name='author-stats'),
]

# Note: If you want API versioning, add this to your main urls.py:
# path('api/v1/', include('api.urls'))