# api/admin.py

from django.contrib import admin
from .models import Author, Book

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Author model.
    """
    list_display = ('name', 'book_count')
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Book model.
    """
    list_display = ('title', 'author', 'publication_year', 'is_recent')
    list_filter = ('publication_year', 'author')
    search_fields = ('title', 'author__name')
    ordering = ('-publication_year', 'title')
    autocomplete_fields = ('author',)