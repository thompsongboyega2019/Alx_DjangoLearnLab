from django.contrib import admin
from .models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'publication_year', 'isbn']
    list_filter = ['publication_year', 'author']
    search_fields = ['title', 'author', 'isbn']
    ordering = ['title']