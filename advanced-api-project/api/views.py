# api/views.py

from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .models import Author, Book
from .serializers import (
    AuthorSerializer, 
    BookSerializer, 
    AuthorBasicSerializer,
    BookCreateSerializer
)
from .filters import BookFilter

# ========================
# ENHANCED BOOK VIEWS WITH FILTERING, SEARCHING, AND ORDERING
# ========================

class BookListView(generics.ListAPIView):
    """
    Enhanced ListView for Books with filtering, searching, and ordering capabilities.
    
    FILTERING CAPABILITIES:
    - Filter by title (exact match): ?title=Book Title
    - Filter by title (contains): ?title_contains=harry
    - Filter by author ID: ?author=1
    - Filter by author name: ?author_name=rowling
    - Filter by publication year: ?publication_year=1997
    - Filter by year range: ?year_from=1990&year_to=2000
    
    SEARCH FUNCTIONALITY:
    - Search across title and author name: ?search=potter
    
    ORDERING OPTIONS:
    - Order by title: ?ordering=title
    - Order by publication year: ?ordering=publication_year
    - Order by author name: ?ordering=author__name
    - Reverse ordering (add minus): ?ordering=-publication_year
    
    EXAMPLE REQUESTS:
    - GET /api/books/ - All books
    - GET /api/books/?title_contains=harry - Books with "harry" in title
    - GET /api/books/?author_name=rowling - Books by authors with "rowling" in name
    - GET /api/books/?year_from=2000 - Books published from 2000 onwards
    - GET /api/books/?search=potter - Search "potter" in title and author
    - GET /api/books/?ordering=-publication_year - Order by year (newest first)
    - GET /api/books/?search=fantasy&ordering=title - Search and order combined
    """
    
    queryset = Book.objects.all().select_related('author')
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]
    
    # Configure the three filter backends
    filter_backends = [
        DjangoFilterBackend,  # For field-based filtering
        SearchFilter,         # For text-based searching
        OrderingFilter,       # For ordering/sorting
    ]
    
    # Configure filtering using our custom FilterSet
    filterset_class = BookFilter
    
    # Configure search functionality
    search_fields = [
        'title',           # Search in book title
        'author__name',    # Search in author name (related field)
    ]
    
    # Configure ordering options
    ordering_fields = [
        'title',           # Allow ordering by title
        'publication_year', # Allow ordering by publication year
        'author__name',    # Allow ordering by author name
    ]
    
    # Set default ordering
    ordering = ['-publication_year', 'title']  # Default: newest books first, then by title


class BookDetailView(generics.RetrieveAPIView):
    """
    DetailView for retrieving a single book by ID.
    
    URL: GET /api/books/<int:pk>/
    """
    queryset = Book.objects.all().select_related('author')
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]


class BookCreateView(generics.CreateAPIView):
    """
    CreateView for adding a new book.
    
    URL: POST /api/books/create/
    """
    queryset = Book.objects.all()
    serializer_class = BookCreateSerializer
    permission_classes = [IsAuthenticated]


class BookUpdateView(generics.UpdateAPIView):
    """
    UpdateView for modifying an existing book.
    
    URL: PUT/PATCH /api/books/update/<int:pk>/
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]


class BookDeleteView(generics.DestroyAPIView):
    """
    DeleteView for removing a book.
    
    URL: DELETE /api/books/delete/<int:pk>/
    """
    queryset = Book.objects.all()
    permission_classes = [IsAuthenticated]


# ========================
# AUTHOR VIEWS (Basic implementation)
# ========================

class AuthorListView(generics.ListAPIView):
    """
    ListView for authors (basic implementation).
    
    URL: GET /api/authors/
    """
    queryset = Author.objects.all().prefetch_related('books')
    serializer_class = AuthorSerializer
    permission_classes = [permissions.AllowAny]


class AuthorDetailView(generics.RetrieveAPIView):
    """
    DetailView for retrieving a single author.
    
    URL: GET /api/authors/<int:pk>/
    """
    queryset = Author.objects.all().prefetch_related('books')
    serializer_class = AuthorSerializer
    permission_classes = [permissions.AllowAny]


class AuthorCreateView(generics.CreateAPIView):
    """
    CreateView for adding a new author.
    
    URL: POST /api/authors/create/
    """
    queryset = Author.objects.all()
    serializer_class = AuthorBasicSerializer
    permission_classes = [IsAuthenticated]


# ========================
# CUSTOM FUNCTION-BASED VIEWS (Optional)
# ========================

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def book_search(request):
    """
    Custom search endpoint with advanced filtering.
    
    This demonstrates how you can create custom search logic
    beyond the standard DRF filtering capabilities.
    
    URL: GET /api/books/search/
    """
    query = request.query_params.get('q', '')
    min_year = request.query_params.get('min_year')
    max_year = request.query_params.get('max_year')
    
    books = Book.objects.select_related('author')
    
    if query:
        books = books.filter(
            Q(title__icontains=query) | 
            Q(author__name__icontains=query)
        )
    
    if min_year:
        books = books.filter(publication_year__gte=min_year)
    
    if max_year:
        books = books.filter(publication_year__lte=max_year)
    
    books = books[:20]  # Limit results
    
    serializer = BookSerializer(books, many=True)
    
    return Response({
        'query': query,
        'results_count': len(serializer.data),
        'results': serializer.data
    })


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def author_statistics(request):
    """
    Statistics endpoint for authors.
    
    URL: GET /api/authors/stats/
    """
    from django.db.models import Count, Min, Max
    
    stats = Author.objects.aggregate(
        total_authors=Count('id'),
        total_books=Count('books')
    )
    
    return Response(stats)