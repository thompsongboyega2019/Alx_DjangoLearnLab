from models import Book, Author, Librarian, Library

books_by_author = Book.objects.filter(author__name='Author Name')
library = Library.objects.get(name='Main City Library')
books_in_library = library.books.all()
librarian = Library.objects.get(name='Main City Library').librarian
