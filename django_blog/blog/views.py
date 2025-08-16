from .models import Comment
from .forms import CommentForm
from django.urls import reverse, reverse_lazy
# --- COMMENT VIEWS ---
from django.views.generic.edit import CreateView, UpdateView, DeleteView

class CommentCreateView(LoginRequiredMixin, CreateView):
	model = Comment
	form_class = CommentForm
	template_name = 'blog/comment_form.html'

	def form_valid(self, form):
		form.instance.author = self.request.user
		form.instance.post_id = self.kwargs['post_id']
		return super().form_valid(form)

	def get_success_url(self):
		return reverse('post-detail', kwargs={'pk': self.kwargs['post_id']})

class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Comment
	form_class = CommentForm
	template_name = 'blog/comment_form.html'

	def get_success_url(self):
		return reverse('post-detail', kwargs={'pk': self.object.post.pk})

	def test_func(self):
		return self.request.user == self.get_object().author

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Comment
	template_name = 'blog/comment_confirm_delete.html'

	def get_success_url(self):
		return reverse_lazy('post-detail', kwargs={'pk': self.object.post.pk})

	def test_func(self):
		return self.request.user == self.get_object().author
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Post
from .forms import PostForm

# List all posts
class PostListView(ListView):
	model = Post
	template_name = 'blog/posts/post_list.html'
	context_object_name = 'posts'
	ordering = ['-published_date']

# View a single post
class PostDetailView(DetailView):
	model = Post
	template_name = 'blog/posts/post_detail.html'

# Create a new post
class PostCreateView(LoginRequiredMixin, CreateView):
	model = Post
	form_class = PostForm
	template_name = 'blog/posts/post_form.html'

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

# Update a post
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Post
	form_class = PostForm
	template_name = 'blog/posts/post_form.html'

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

	def test_func(self):
		post = self.get_object()
		return self.request.user == post.author

# Delete a post
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Post
	template_name = 'blog/posts/post_confirm_delete.html'
	success_url = '/posts/'

	def test_func(self):
		post = self.get_object()
		return self.request.user == post.author
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
