from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required
from django.contrib import messages
from django.urls import reverse
from .models import Book
from .form import BookForm  # Assuming you have a BookForm

def book_list(request):
    """View to display all books - no permission required for viewing"""
    books = Book.objects.all()
    return render(request, 'relationship_app/book_list.html', {'books': books})

@permission_required('relationship_app.can_add_book')
def add_book(request):
    """View to add a new book - requires can_add_book permission"""
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Book added successfully!')
            return redirect('book_list')
    else:
        form = BookForm()
    
    return render(request, 'relationship_app/add_book.html', {'form': form})

@permission_required('relationship_app.can_change_book')
def edit_book(request, book_id):
    """View to edit an existing book - requires can_change_book permission"""
    book = get_object_or_404(Book, id=book_id)
    
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, 'Book updated successfully!')
            return redirect('book_list')
    else:
        form = BookForm(instance=book)
    
    return render(request, 'relationship_app/edit_book.html', {
        'form': form, 
        'book': book
    })

@permission_required('relationship_app.can_delete_book')
def delete_book(request, book_id):
    """View to delete a book - requires can_delete_book permission"""
    book = get_object_or_404(Book, id=book_id)
    
    if request.method == 'POST':
        book.delete()
        messages.success(request, 'Book deleted successfully!')
        return redirect('book_list')
    
    return render(request, 'relationship_app/delete_book.html', {'book': book})

def book_detail(request, book_id):
    """View to display book details - no permission required for viewing"""
    book = get_object_or_404(Book, id=book_id)
    return render(request, 'relationship_app/book_detail.html', {'book': book})
