from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year', 'isbn']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.TextInput(attrs={'class': 'form-control'}),
            'publication_year': forms.NumberInput(attrs={'class': 'form-control'}),
            'isbn': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def clean_isbn(self):
        isbn = self.cleaned_data.get('isbn')
        if isbn and len(isbn) not in [10, 13]:
            raise forms.ValidationError("ISBN must be 10 or 13 characters long.")
        return isbn