# api/views.py

from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .models import Author, Book
from .serializers import (
    AuthorSerializer, 
    BookSerializer, 
    AuthorBasicSerializer,
    BookCreateSerializer
)

# ========================
# BOOK VIEWS - Generic Views for CRUD Operations
# ========================

class BookListView(generics.ListAPIView):
    """
    Generic ListView for retrieving all books.
    
    This view handles GET requests to retrieve a list of all books in the database.
    It supports filtering, ordering, and pagination out of the box.
    
    Features:
    - Public access (no authentication required for reading)
    - Supports query parameters for filtering
    - Automatic pagination
    - Ordering by publication year (newest first)
    
    URL: GET /api/books/
    """
    queryset = Book.objects.all().select_related('author')  # Optimize database queries
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]  # Public read access
    
    # Enable filtering and ordering
    filterset_fields = ['author', 'publication_year']
    ordering_fields = ['publication_year', 'title', 'author__name']
    ordering = ['-publication_year', 'title']  # Default ordering
    
    def get_queryset(self):
        """
        Customize queryset with additional filtering options.
        
        Supports query parameters:
        - search: Search in title and author name
        - year_from: Books published from this year
        - year_to: Books published up to this year
        """
        queryset = super().get_queryset()
        
        # Search functionality
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | 
                Q(author__name__icontains=search)
            )
        
        # Year range filtering
        year_from = self.request.query_params.get('year_from')
        year_to = self.request.query_params.get('year_to')
        
        if year_from:
            queryset = queryset.filter(publication_year__gte=year_from)
        if year_to:
            queryset = queryset.filter(publication_year__lte=year_to)
        
        return queryset


class BookDetailView(generics.RetrieveAPIView):
    """
    Generic DetailView for retrieving a single book by ID.
    
    This view handles GET requests to retrieve a specific book instance.
    It provides detailed information about a single book including author details.
    
    Features:
    - Public access (no authentication required)
    - Automatic 404 handling for non-existent books
    - Optimized database queries with select_related
    
    URL: GET /api/books/<int:pk>/
    """
    queryset = Book.objects.all().select_related('author')
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]  # Public read access
    lookup_field = 'pk'  # Use primary key for lookup
    
    def retrieve(self, request, *args, **kwargs):
        """
        Custom retrieve method with additional metadata.
        
        Adds extra information to the response such as related books
        by the same author.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        
        # Add related books by the same author
        related_books = Book.objects.filter(
            author=instance.author
        ).exclude(pk=instance.pk)[:5]  # Limit to 5 related books
        
        related_serializer = BookSerializer(related_books, many=True)
        
        response_data = serializer.data
        response_data['related_books'] = related_serializer.data
        
        return Response(response_data)


class BookCreateView(generics.CreateAPIView):
    """
    Generic CreateView for adding a new book.
    
    This view handles POST requests to create new book instances.
    It includes comprehensive validation and proper error handling.
    
    Features:
    - Requires authentication (only authenticated users can create books)
    - Custom validation through serializers
    - Automatic HTTP 201 Created response on success
    - Detailed error messages on validation failure
    
    URL: POST /api/books/
    """
    queryset = Book.objects.all()
    serializer_class = BookCreateSerializer
    permission_classes = [IsAuthenticated]  # Require authentication
    
    def perform_create(self, serializer):
        """
        Custom create logic with additional processing.
        
        This method is called after validation but before saving.
        It can be used to add custom logic like logging, notifications, etc.
        """
        # Save the book instance
        book = serializer.save()
        
        # Add any custom post-creation logic here
        # For example: logging, sending notifications, etc.
        print(f"New book created: {book.title} by {book.author.name}")
        
        return book
    
    def create(self, request, *args, **kwargs):
        """
        Custom create method with enhanced response.
        
        Provides a more detailed response including the created book data
        and success message.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Perform the creation
        book = self.perform_create(serializer)
        
        # Return detailed response
        response_serializer = BookSerializer(book)
        
        return Response({
            'message': 'Book created successfully',
            'book': response_serializer.data
        }, status=status.HTTP_201_CREATED)


class BookUpdateView(generics.UpdateAPIView):
    """
    Generic UpdateView for modifying an existing book.
    
    This view handles PUT and PATCH requests to update book instances.
    It supports both full updates (PUT) and partial updates (PATCH).
    
    Features:
    - Requires authentication (only authenticated users can update books)
    - Supports both PUT (full update) and PATCH (partial update)
    - Comprehensive validation
    - Custom update logic
    
    URL: PUT/PATCH /api/books/<int:pk>/
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # Require authentication
    
    def perform_update(self, serializer):
        """
        Custom update logic with additional processing.
        
        This method is called after validation but before saving.
        """
        # Save the updated book instance
        book = serializer.save()
        
        # Add any custom post-update logic here
        print(f"Book updated: {book.title} by {book.author.name}")
        
        return book
    
    def update(self, request, *args, **kwargs):
        """
        Custom update method with enhanced response.
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        
        # Perform the update
        book = self.perform_update(serializer)
        
        # Return detailed response
        return Response({
            'message': 'Book updated successfully',
            'book': serializer.data
        })
    
    def partial_update(self, request, *args, **kwargs):
        """Handle PATCH requests for partial updates."""
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)


class BookDeleteView(generics.DestroyAPIView):
    """
    Generic DeleteView for removing a book.
    
    This view handles DELETE requests to remove book instances from the database.
    It includes proper permission checking and custom deletion logic.
    
    Features:
    - Requires authentication (only authenticated users can delete books)
    - Soft delete option (can be implemented if needed)
    - Custom deletion logic
    - Proper HTTP 204 No Content response
    
    URL: DELETE /api/books/<int:pk>/
    """
    queryset = Book.objects.all()
    permission_classes = [IsAuthenticated]  # Require authentication
    
    def perform_destroy(self, instance):
        """
        Custom deletion logic.
        
        This method can be overridden to implement soft deletion,
        logging, or other custom logic before actual deletion.
        """
        # Log the deletion
        print(f"Deleting book: {instance.title} by {instance.author.name}")
        
        # Perform the actual deletion
        instance.delete()
    
    def destroy(self, request, *args, **kwargs):
        """
        Custom destroy method with enhanced response.
        """
        instance = self.get_object()
        book_info = {
            'title': instance.title,
            'author': instance.author.name,
            'id': instance.id
        }
        
        self.perform_destroy(instance)
        
        return Response({
            'message': 'Book deleted successfully',
            'deleted_book': book_info
        }, status=status.HTTP_204_NO_CONTENT)


# ========================
# AUTHOR VIEWS - Additional Generic Views
# ========================

class AuthorListView(generics.ListAPIView):
    """
    Generic ListView for retrieving all authors with their books.
    
    This view provides a comprehensive list of all authors including
    their associated books using nested serialization.
    
    URL: GET /api/authors/
    """
    queryset = Author.objects.all().prefetch_related('books')
    serializer_class = AuthorSerializer
    permission_classes = [permissions.AllowAny]
    ordering = ['name']
    
    def get_queryset(self):
        """Add search functionality for authors."""
        queryset = super().get_queryset()
        
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(name__icontains=search)
        
        return queryset


class AuthorDetailView(generics.RetrieveAPIView):
    """
    Generic DetailView for retrieving a single author with all books.
    
    URL: GET /api/authors/<int:pk>/
    """
    queryset = Author.objects.all().prefetch_related('books')
    serializer_class = AuthorSerializer
    permission_classes = [permissions.AllowAny]


class AuthorCreateView(generics.CreateAPIView):
    """
    Generic CreateView for adding a new author.
    
    URL: POST /api/authors/
    """
    queryset = Author.objects.all()
    serializer_class = AuthorBasicSerializer
    permission_classes = [IsAuthenticated]


# ========================
# CUSTOM FUNCTION-BASED VIEWS (Alternative Implementation)
# ========================

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def book_search(request):
    """
    Custom function-based view for advanced book searching.
    
    This view demonstrates how to create custom endpoints that don't
    fit the standard CRUD pattern.
    
    URL: GET /api/books/search/
    
    Query Parameters:
    - q: Search query (searches title and author name)
    - min_year: Minimum publication year
    - max_year: Maximum publication year
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
    
    # Limit results
    books = books[:20]
    
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
    Custom view to provide author statistics.
    
    URL: GET /api/authors/stats/
    """
    from django.db.models import Count, Min, Max
    
    stats = Author.objects.aggregate(
        total_authors=Count('id'),
        total_books=Count('books'),
        earliest_publication=Min('books__publication_year'),
        latest_publication=Max('books__publication_year')
    )
    
    # Top authors by book count
    top_authors = Author.objects.annotate(
        book_count=Count('books')
    ).order_by('-book_count')[:5]
    
    top_authors_data = AuthorBasicSerializer(top_authors, many=True).data
    
    return Response({
        'statistics': stats,
        'top_authors': top_authors_data
    })