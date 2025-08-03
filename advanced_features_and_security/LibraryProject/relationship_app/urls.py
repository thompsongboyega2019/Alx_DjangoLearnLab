
from django.urls import path
from . import views

urlpatterns = [
    # Book list view - no permissions required
    path('books/', views.book_list, name='book_list'),
    
    # Book detail view - no permissions required
    path('books/<int:book_id>/', views.book_detail, name='book_detail'),
    
    # Secured views with permission requirements
    path('add_book/', views.add_book, name='add_book'),
    path('edit_book/', views.edit_book, name='edit_book'),
    path('books/<int:book_id>/delete/', views.delete_book, name='delete_book'),
]