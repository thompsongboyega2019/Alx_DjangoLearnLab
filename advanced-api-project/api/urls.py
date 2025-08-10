# api/urls.py

from django.urls import path, include
from . import views

# Define API version
API_VERSION = 'v1'

urlpatterns = [
    # Book CRUD endpoints
    path('books/', views.BookListView.as_view(), name='book-list'),
    path('books/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),
    path('books/create/', views.BookCreateView.as_view(), name='book-create'),
    path('books/<int:pk>/update/', views.BookUpdateView.as_view(), name='book-update'),
    path('books/<int:pk>/delete/', views.BookDeleteView.as_view(), name='book-delete'),
    
    # Author CRUD endpoints
    path('authors/', views.AuthorListView.as_view(), name='author-list'),
    path('authors/<int:pk>/', views.AuthorDetailView.as_view(), name='author-detail'),
    path('authors/create/', views.AuthorCreateView.as_view(), name='author-create'),
    
    # Custom endpoints
    path('books/search/', views.book_search, name='book-search'),
    path('authors/stats/', views.author_statistics, name='author-stats'),
]

# Add API versioning (optional but recommended)
versioned_urlpatterns = [
    path(f'{API_VERSION}/', include(urlpatterns)),
]