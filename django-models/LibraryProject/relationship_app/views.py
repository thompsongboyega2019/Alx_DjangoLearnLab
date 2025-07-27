# from django.shortcuts import render, redirect
# from django.views.generic.detail import DetailView
# from .models import Library, Book
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth import login
# # from django.urls import reverse_lazy
# # from django.views.generic import CreateView



# # Create your views here.
# def list_books(request):
#     book_list = Book.objects.all()
#     return render(request, 'relationship_app/list_books.html', {'books': book_list} )



# class LibraryDetailView(DetailView):
#     model = Library
#     template_name = 'relationship_app/library_detail.html'
#     context_object_name = 'library'

# # class SignUpView(CreateView):
# #     form_class = UserCreationForm
# #     success_url = reverse_lazy('relationship_app/login.html')
# #     template_name = 'relationship_app/register.html'

# def register(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()  # Save user to DB
#             login(request, user)  # Log the user in immediately
#             return redirect('relationship_app/login.html')  # Redirect to a post-login page
#     else:
#         form = UserCreationForm()
#     return render(request, 'relationship_app/register.html', {'form': form})



from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseForbidden
from django.core.exceptions import PermissionDenied


def is_admin(user):
    """
    Check if the user has Admin role.
    """
    return user.is_authenticated and hasattr(user, 'profile') and user.profile.role == 'Admin'


def is_librarian(user):
    """
    Check if the user has Librarian role.
    """
    return user.is_authenticated and hasattr(user, 'profile') and user.profile.role == 'Librarian'


def is_member(user):
    """
    Check if the user has Member role.
    """
    return user.is_authenticated and hasattr(user, 'profile') and user.profile.role == 'Member'


@login_required
@user_passes_test(is_admin, login_url='/login/')
def admin_view(request):
    """
    Admin-only view that displays administrative content.
    Only users with 'Admin' role can access this view.
    """
    context = {
        'user': request.user,
        'role': request.user.profile.role,
        'page_title': 'Admin Dashboard',
        'welcome_message': f'Welcome, {request.user.username}! You have administrative privileges.',
    }
    return render(request, 'relationship_app/admin_view.html', context)


@login_required
@user_passes_test(is_librarian, login_url='/login/')
def librarian_view(request):
    """
    Librarian-only view that displays librarian-specific content.
    Only users with 'Librarian' role can access this view.
    """
    context = {
        'user': request.user,
        'role': request.user.profile.role,
        'page_title': 'Librarian Dashboard',
        'welcome_message': f'Welcome, {request.user.username}! You can manage library resources.',
    }
    return render(request, 'relationship_app/librarian_view.html', context)


@login_required
@user_passes_test(is_member, login_url='/login/')
def member_view(request):
    """
    Member-only view that displays member-specific content.
    Only users with 'Member' role can access this view.
    """
    context = {
        'user': request.user,
        'role': request.user.profile.role,
        'page_title': 'Member Dashboard',
        'welcome_message': f'Welcome, {request.user.username}! Explore available resources.',
    }
    return render(request, 'relationship_app/member_view.html', context)


# Additional utility view for role management (optional)
@login_required
def dashboard(request):
    """
    General dashboard that redirects users based on their role.
    """
    if hasattr(request.user, 'profile'):
        role = request.user.profile.role
        if role == 'Admin':
            return redirect('admin_view')
        elif role == 'Librarian':
            return redirect('librarian_view')
        elif role == 'Member':
            return redirect('member_view')
    
    # If no profile exists, create one with default Member role
    from .models import UserProfile
    profile = UserProfile.objects.create(user=request.user, role='Member')
    return redirect('member_view')
