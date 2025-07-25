from models import Book, Author, Librarian, Library

author_name = 'Author Name'
author = Author.objects.get(name=author_name)
books_by_author = Book.objects.filter(author=author)

library_name = "Main City Library"
library = Library.objects.get(name=library_name)
books_in_library = library.books.all()
librarian = Librarian.objects.get(library=library)
