"""
Unit tests for Book API endpoints in the Django REST Framework project.

Covers CRUD operations, filtering, searching, ordering, and permission/authentication checks.
"""
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from .models import Book

class BookAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client = APIClient()
        self.book1 = Book.objects.create(title='Book One', author='Author A', published_date='2020-01-01', price=10.99)
        self.book2 = Book.objects.create(title='Book Two', author='Author B', published_date='2021-01-01', price=12.99)
        self.list_url = reverse('book-list')

    def test_create_book_authenticated(self):
        self.client.login(username='testuser', password='testpass')
        data = {'title': 'Book Three', 'author': 'Author C', 'published_date': '2022-01-01', 'price': 15.99}
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)
        self.assertEqual(Book.objects.last().title, 'Book Three')

    def test_create_book_unauthenticated(self):
        data = {'title': 'Book Four', 'author': 'Author D', 'published_date': '2023-01-01', 'price': 18.99}
        response = self.client.post(self.list_url, data, format='json')
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    def test_list_books(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_retrieve_book(self):
        url = reverse('book-detail', args=[self.book1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.book1.title)

    def test_update_book(self):
        self.client.login(username='testuser', password='testpass')
        url = reverse('book-detail', args=[self.book1.id])
        data = {'title': 'Book One Updated', 'author': 'Author A', 'published_date': '2020-01-01', 'price': 11.99}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Book One Updated')

    def test_delete_book(self):
        self.client.login(username='testuser', password='testpass')
        url = reverse('book-detail', args=[self.book2.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(id=self.book2.id).exists())

    def test_filter_books_by_author(self):
        response = self.client.get(self.list_url, {'author': 'Author A'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['author'], 'Author A')

    def test_search_books_by_title(self):
        response = self.client.get(self.list_url, {'search': 'Book One'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(any('Book One' in book['title'] for book in response.data))

    def test_order_books_by_price(self):
        response = self.client.get(self.list_url, {'ordering': 'price'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        prices = [book['price'] for book in response.data]
        self.assertEqual(prices, sorted(prices))

    def test_permissions_enforced(self):
        url = reverse('book-detail', args=[self.book1.id])
        response = self.client.delete(url)
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

"""
Testing Documentation:
- Tests cover CRUD, filtering, searching, ordering, and permissions for Book endpoints.
- Run tests with: python manage.py test api
- Ensure test database is used (Django does this automatically).
- Review output for failures and fix any issues in code or tests.
"""
