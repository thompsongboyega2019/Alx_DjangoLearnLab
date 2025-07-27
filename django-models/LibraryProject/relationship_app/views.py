from django.shortcuts import render, redirect
from django.views.generic.detail import DetailView
from .models import Library, Book
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
# from django.urls import reverse_lazy
# from django.views.generic import CreateView



# Create your views here.
def list_books(request):
    book_list = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': book_list} )



class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

# class SignUpView(CreateView):
#     form_class = UserCreationForm
#     success_url = reverse_lazy('relationship_app/login.html')
#     template_name = 'relationship_app/register.html'

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save user to DB
            login(request, user)  # Log the user in immediately
            return redirect('relationship_app/login.html')  # Redirect to a post-login page
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})
