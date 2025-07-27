# from django.urls import path
# # from .views import list_books, LibraryDetailView, SignUpView
# from . import views
# from django.contrib.auth.views import LoginView, LogoutView



# urlpatterns = [
#     # path('books', list_books, name="list_of_books"),
#     # path('register', SignUpView.as_view(), name='register'),
#     # path('library', LibraryDetailView.as_view(), name='library'  ),
#     path('register', views.register, name='register'),
#     path('login', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
#     path('', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
#     path('admin/', views.admin_view, name='admin_view'),
#     path('librarian/', views.librarian_view, name='librarian_view'),
#     path('member/', views.member_view, name='member_view'),
    
    
# ]



from django.urls import path
from . import views

urlpatterns = [
    # Book list view - no permissions required
    path('books/', views.book_list, name='book_list'),
    
    # Book detail view - no permissions required
    path('books/<int:book_id>/', views.book_detail, name='book_detail'),
    
    # Secured views with permission requirements
    path('books/add/', views.add_book, name='add_book'),
    path('books/<int:book_id>/edit/', views.edit_book, name='edit_book'),
    path('books/<int:book_id>/delete/', views.delete_book, name='delete_book'),
]