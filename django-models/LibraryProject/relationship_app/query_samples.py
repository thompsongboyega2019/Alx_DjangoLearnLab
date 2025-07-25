from models import Book, Author, Librarian, Library

books_by_author = Book.objects.filter(author__name='Author Name')
books_in_library = Book.objects.filter(library__name='Main City Library')
librarian = Library.objects.get(name='Main City Library').librarian
