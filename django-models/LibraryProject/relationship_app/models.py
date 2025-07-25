from django.db import models

# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=255)

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

class Library(models.Model):
    name = models.CharField(max_length=255)
    books = models.ManyToManyField(Book, related_name='book')

class Librarian(models.Model):
    name = models.CharField(max_length=255)
    library = models.OneToOneField(Library, on_delete=models.CASCADE)