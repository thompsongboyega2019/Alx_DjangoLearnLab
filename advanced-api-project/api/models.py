# api/models.py

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import datetime

class Author(models.Model):
   
    name = models.CharField(
        max_length=255,
        help_text="Full name of the author"
    )
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Author'
        verbose_name_plural = 'Authors'
    
    def __str__(self):
        """String representation of the Author model."""
        return self.name
    
    @property
    def book_count(self):
        """Return the number of books written by this author."""
        return self.books.count()


class Book(models.Model):
    """
    Book model to store information about books and their relationships to authors.
    
    This model represents individual books in our library system.
    Each book is linked to exactly one author through a foreign key relationship,
    implementing the many-to-one relationship from books to authors.
    
    Fields:
    - title: CharField to store the book's title
    - publication_year: IntegerField for the year the book was published
    - author: ForeignKey linking to the Author model
    
    The relationship works as follows:
    - Each Book instance has one Author (many-to-one from Book to Author)
    - Each Author can have multiple Books (one-to-many from Author to Book)
    - This is implemented using Django's ForeignKey with related_name='books'
    """
    title = models.CharField(
        max_length=255,
        help_text="Title of the book"
    )
    
    publication_year = models.IntegerField(
        validators=[
            MinValueValidator(1000),  # Reasonable minimum year
            MaxValueValidator(datetime.now().year)  # Cannot be in the future
        ],
        help_text="Year the book was published"
    )
    
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name='books',
        help_text="Author who wrote this book"
    )
    
    class Meta:
        ordering = ['-publication_year', 'title']
        verbose_name = 'Book'
        verbose_name_plural = 'Books'
        # Ensure no duplicate titles by the same author in the same year
        unique_together = ['title', 'author', 'publication_year']
    
    def __str__(self):
        """String representation of the Book model."""
        return f"{self.title} ({self.publication_year}) by {self.author.name}"
    
    @property
    def is_recent(self):
        """Check if the book was published in the last 5 years."""
        current_year = datetime.now().year
        return current_year - self.publication_year <= 5