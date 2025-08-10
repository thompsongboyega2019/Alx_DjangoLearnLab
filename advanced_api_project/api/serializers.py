# api/serializers.py

from rest_framework import serializers
from datetime import datetime
from .models import Author, Book

class BookSerializer(serializers.ModelSerializer):
    """
    Custom serializer for the Book model with advanced validation.
    
    This serializer handles the serialization and deserialization of Book instances.
    It includes custom validation to ensure data integrity, specifically preventing
    books from having publication years in the future.
    
    Features:
    - Serializes all Book model fields
    - Custom validation for publication_year
    - Nested author information (when used in AuthorSerializer)
    - Proper error handling and validation messages
    """
    
    # Optional: Add author name as a read-only field for easier API consumption
    author_name = serializers.CharField(source='author.name', read_only=True)
    
    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author', 'author_name']
        extra_kwargs = {
            'author': {'write_only': False}  # Allow both read and write
        }
    
    def validate_publication_year(self, value):
        """
        Custom validation for publication_year field.
        
        Ensures that the publication year is not in the future.
        This prevents users from creating books with invalid publication dates.
        
        Args:
            value (int): The publication year to validate
            
        Returns:
            int: The validated publication year
            
        Raises:
            serializers.ValidationError: If the year is in the future
        """
        current_year = datetime.now().year
        
        if value > current_year:
            raise serializers.ValidationError(
                f"Publication year cannot be in the future. "
                f"Current year is {current_year}, but got {value}."
            )
        
        # Additional validation: reasonable minimum year
        if value < 1000:
            raise serializers.ValidationError(
                "Publication year must be a valid year (minimum 1000)."
            )
        
        return value
    
    def validate(self, data):
        """
        Object-level validation for the entire Book instance.
        
        This method can be used for validation that requires access to multiple fields.
        """
        # Example: Additional validation logic can be added here
        return data


class AuthorSerializer(serializers.ModelSerializer):
    """
    Custom serializer for the Author model with nested Book serialization.
    
    This serializer demonstrates advanced Django REST Framework concepts:
    - Nested serialization of related objects (books)
    - Dynamic inclusion of related data
    - Custom fields and methods
    - Handling of one-to-many relationships
    
    The serializer includes a nested BookSerializer to automatically serialize
    all books related to an author. This allows API consumers to get complete
    author information including their books in a single request.
    
    Relationship Handling:
    - Uses the 'books' related_name from the Book model's ForeignKey
    - Serializes books as a nested list within the author data
    - Provides both read and write capabilities for nested data
    """
    
    # Nested serialization of related books
    # This creates a nested representation of all books by this author
    books = BookSerializer(many=True, read_only=True)
    
    # Additional computed field: total number of books
    book_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Author
        fields = ['id', 'name', 'books', 'book_count']
    
    def get_book_count(self, obj):
        """
        Custom method field to get the count of books by this author.
        
        Args:
            obj (Author): The Author instance being serialized
            
        Returns:
            int: Number of books written by this author
        """
        return obj.books.count()
    
    def to_representation(self, instance):
        """
        Custom representation method to modify the serialized output.
        
        This method can be overridden to customize how the serialized data appears.
        For example, we could conditionally include or exclude certain fields,
        format data differently, or add computed values.
        
        Args:
            instance (Author): The Author instance being serialized
            
        Returns:
            dict: The serialized representation of the author
        """
        representation = super().to_representation(instance)
        
        # Example: Add metadata about the author's books
        if representation['books']:
            years = [book['publication_year'] for book in representation['books']]
            representation['publication_year_range'] = {
                'earliest': min(years),
                'latest': max(years)
            }
        
        return representation


# Alternative serializer for cases where we don't need nested books
class AuthorBasicSerializer(serializers.ModelSerializer):
    """
    Basic Author serializer without nested books.
    
    This can be used when we only need author information without the related books,
    which can improve performance for large datasets or when books are not needed.
    """
    book_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Author
        fields = ['id', 'name', 'book_count']
    
    def get_book_count(self, obj):
        return obj.books.count()


# Serializer for creating books with author information
class BookCreateSerializer(serializers.ModelSerializer):
    """
    Specialized serializer for creating books with enhanced validation.
    
    This serializer can be used specifically for book creation endpoints
    where we might need different validation or field requirements.
    """
    
    class Meta:
        model = Book
        fields = ['title', 'publication_year', 'author']
    
    def validate_publication_year(self, value):
        """Same validation as BookSerializer."""
        current_year = datetime.now().year
        if value > current_year:
            raise serializers.ValidationError(
                f"Publication year cannot be in the future. Current year is {current_year}."
            )
        if value < 1000:
            raise serializers.ValidationError(
                "Publication year must be a valid year (minimum 1000)."
            )
        return value
    
    def create(self, validated_data):
        """
        Custom create method with additional logic.
        
        This method can include custom logic for book creation,
        such as logging, sending notifications, or other business logic.
        """
        book = Book.objects.create(**validated_data)
        # Add any custom post-creation logic here
        return book