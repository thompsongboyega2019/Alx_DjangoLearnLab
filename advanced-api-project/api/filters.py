# api/filters.py

import django_filters
from .models import Book, Author

class BookFilter(django_filters.FilterSet):
    """
    Custom filter for Book model with comprehensive filtering options.
    
    This FilterSet provides multiple ways to filter books:
    - Exact matches and case-insensitive searches
    - Range filtering for publication years
    - Author-based filtering
    """
    
    # Title filtering
    title = django_filters.CharFilter(
        field_name='title', 
        lookup_expr='exact',
        help_text='Filter by exact title match'
    )
    
    title_contains = django_filters.CharFilter(
        field_name='title', 
        lookup_expr='icontains',
        help_text='Filter by title containing text (case-insensitive)'
    )
    
    # Author filtering
    author = django_filters.ModelChoiceFilter(
        queryset=Author.objects.all(),
        help_text='Filter by author ID'
    )
    
    author_name = django_filters.CharFilter(
        field_name='author__name',
        lookup_expr='icontains',
        help_text='Filter by author name (case-insensitive)'
    )
    
    # Publication year filtering
    publication_year = django_filters.NumberFilter(
        field_name='publication_year',
        help_text='Filter by exact publication year'
    )
    
    year_from = django_filters.NumberFilter(
        field_name='publication_year',
        lookup_expr='gte',
        help_text='Filter books published from this year onwards'
    )
    
    year_to = django_filters.NumberFilter(
        field_name='publication_year',
        lookup_expr='lte',
        help_text='Filter books published up to this year'
    )
    
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year']