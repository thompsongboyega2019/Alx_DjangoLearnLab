# myapp/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required
from .models import Book

@permission_required('myapp.can_view', raise_exception=True)
def article_list(request):
    articles = Book.objects.all()
    return render(request, 'myapp/article_list.html', {'articles': articles})

@permission_required('myapp.can_create', raise_exception=True)
def article_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        Book.objects.create(title=title, content=content)
        return redirect('article_list')
    return render(request, 'myapp/article_form.html')

@permission_required('myapp.can_edit', raise_exception=True)
def article_edit(request, pk):
    article = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        article.title = request.POST.get('title')
        article.content = request.POST.get('content')
        article.save()
        return redirect('article_list')
    return render(request, 'myapp/article_form.html', {'article': article})

@permission_required('myapp.can_delete', raise_exception=True)
def article_delete(request, pk):
    article = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        article.delete()
        return redirect('article_list')
    return render(request, 'myapp/article_confirm_delete.html', {'article': article})
