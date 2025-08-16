from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from django.shortcuts import redirect
from .forms import UserRegisterForm, UserUpdateForm

class CustomLoginView(LoginView):
	template_name = 'blog/login.html'

class CustomLogoutView(LogoutView):
	template_name = 'blog/logout.html'

def register(request):
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, 'Registration successful!')
			return redirect('profile')
	else:
		form = UserRegisterForm()
	return render(request, 'blog/register.html', {'form': form})

@login_required
def profile(request):
	if request.method == 'POST':
		form = UserUpdateForm(request.POST, instance=request.user)
		if form.is_valid():
			form.save()
			messages.success(request, 'Profile updated!')
			return redirect('profile')
	else:
		form = UserUpdateForm(instance=request.user)
	return render(request, 'blog/profile.html', {'form': form})
from django.shortcuts import render

# Create your views here.
