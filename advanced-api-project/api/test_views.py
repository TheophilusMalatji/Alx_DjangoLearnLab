from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from datetime import datetime
from .models import Book, Author 
from rest_framework import status


# --- Base Test Setup ---

class BaseAPITestCase(TestCase):
    """Sets up authenticated client, an unauthenticated client, and base data for all tests."""
    def setUp(self):
        # 1. Setup Clients and Users
        self.client = APIClient()
        self.user = User.objects.create_user(username='tester', password='securepassword')
        
        # Create an admin user for permission tests (assuming is_admin=True is needed for IsAdminUser)
        self.admin_user = User.objects.create_user(username='admin', password='adminpassword', is_staff=True)
      

        self.auth_client = APIClient()
        self.auth_client.force_authenticate(user=self.user)
        self.admin_client = APIClient()
        self.admin_client.force_authenticate(user=self.admin_user)
        self.client.login = APIClient()
        

        # 2. Setup Base Data
        self.author_one = Author.objects.create(name="Jane Austen")
        self.author_two = Author.objects.create(name="Charles Dickens")
        
        current_year = datetime.now().year
        self.book_a = Book.objects.create(
            title="Pride and Prejudice",
            author=self.author_one,
            publication_year=current_year - 5
        )
        self.book_b = Book.objects.create(
            title="Sense and Sensibility",
            author=self.author_one,
            publication_year=current_year - 3
        )
        self.book_c = Book.objects.create(
            title="A Tale of Two Cities",
            author=self.author_two,
            publication_year=current_year - 7
        )
        
        self.book_a_pk = self.book_a.pk
        
        # 3. Setup URLs - USING YOUR CUSTOM NAMES
        self.book_list_url = reverse('books')          # GET List
        self.book_create_url = reverse('book-create')  # POST Create
        self.book_delete_url = reverse('book-delete')  # DELETE Destroy
        self.book_update_url = reverse('book-update')  # PUT/PATCH Update

       


# --- Book Tests (CRUD and Validation) ---

class BookTests(BaseAPITestCase):

    # 1. CREATE TESTS (POST /api/books/create)

    def test_create_book_success(self):
        """Tests POST /api/books/create for successful creation (201 status)."""
        valid_payload = {
            'title': 'New Novel',
            'author': self.author_two.pk,
            'publication_year': datetime.now().year
        }
        
        response = self.admin_client.post(self.book_create_url, valid_payload, format='json')
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Book.objects.count(), 4) 

    def test_create_future_date_validation_failure(self):
        """Tests POST validation to block future publication year (400 status)."""
        future_year = datetime.now().year + 1
        invalid_payload = {
            'title': 'Future Book',
            'author': self.author_one.pk,
            'publication_year': future_year
        }
        # Test validation using admin client
        response = self.admin_client.post(self.book_create_url, invalid_payload, format='json')
            
        self.assertEqual(response.status_code, 400) 
        self.assertIn('Publication date can not be future date', str(response.data))
        self.assertEqual(Book.objects.count(), 3) # Count should not change 


    # 2. LIST TEST (GET /api/books/)
    
    def test_list_all_books_success_authenticated(self):
        """Tests GET /api/books/ for listing all records (200 status)."""
        # Test using authenticated client (IsAuthenticatedOrReadOnly allows authenticated GET)
        response = self.auth_client.get(self.book_list_url, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 3)

    # 3. DELETE TEST (DELETE /api/books/delete)

    def test_delete_book_success(self):
        """Tests DELETE /api/books/delete for successful deletion (204 status)."""
        # The view must receive the PK in the payload
        delete_payload = {'pk': self.book_a_pk}
        
        response = self.admin_client.delete(self.book_delete_url, delete_payload, format='json')
        
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Book.objects.count(), 2)
        self.assertFalse(Book.objects.filter(pk=self.book_a_pk).exists())

    # 4. UPDATE TESTS (PUT/PATCH /api/books/update)

    def test_partial_update_book_patch_success(self):
        """Tests PATCH /api/books/update for partial update (200 status)."""
        partial_payload = {'pk': self.book_a_pk,'title': 'Updated Title Only'}
        
        response = self.admin_client.patch(self.book_update_url, partial_payload, format='json')
        
        self.assertEqual(response.status_code, 200)
        self.book_a.refresh_from_db()
        self.assertEqual(self.book_a.title, 'Updated Title Only')

    def test_full_update_future_date_validation_failure(self):
        """Tests PUT validation to block future publication year (400 status)."""
        future_year = datetime.now().year + 1
        invalid_payload = {
            'pk': self.book_a_pk,
            'title': self.book_a.title,
            'author': self.book_a.author.pk,
            'publication_year': future_year 
        }
        
        response = self.admin_client.put(self.book_update_url, invalid_payload, format='json')
        
        self.assertEqual(response.status_code, 400)
        self.assertIn('Publication date can not be future date', str(response.data))
        self.book_a.refresh_from_db()
        self.assertNotEqual(self.book_a.publication_year, future_year)
        
        
# --- Permission/Authentication Tests ---
VALID_PAYLOAD = {
    'title': 'Permission Test Book',
    'author': 1, # Use a valid PK
    'publication_year': datetime.now().year
}
class PermissionTests(BaseAPITestCase):
    """Test all permissions with endpoints"""
    
    # --- Read Access (BookListView) ---
    
    
    def test_list_books_unauthenticated_read_only(self):
        """Tests GET /api/books/ for unauthenticated access (allowed by IsAuthenticatedOrReadOnly)."""
        response = self.client.get(self.book_list_url)
        self.assertEqual(response.status_code, 200) # Should be allowed
        self.assertEqual(len(response.data), 3)

    # --- Write Access (BookCreateView, BookUpdateView, BookDeleteView) ---

    def test_create_denied_unauthenticated(self):
        """Tests POST /api/books/create denied for unauthenticated users (403 Forbidden)."""
        # Use the valid payload
        response = self.client.post(self.book_create_url, VALID_PAYLOAD, format='json') 
        self.assertEqual(response.status_code, 403)       
          
    def test_create_denied_authenticated_non_admin(self):
        """Tests POST /api/books/create denied for standard authenticated users (403 Forbidden)."""
        # Use the valid payload
        response = self.auth_client.post(self.book_create_url, VALID_PAYLOAD, format='json')
        self.assertEqual(response.status_code, 403) 

    def test_delete_denied_unauthenticated(self):
        """Tests DELETE /api/books/delete denied for unauthenticated users (403 Forbidden)."""
        # Use the necessary PK payload
        delete_payload = {'pk': self.book_a_pk} 
        response = self.client.delete(self.book_delete_url, delete_payload, format='json') 
        self.assertEqual(response.status_code, 403)
        
    def test_update_denied_authenticated_non_admin(self):
        """Tests PATCH /api/books/update denied for standard authenticated users (403 Forbidden)."""
        partial_payload = {'pk': self.book_a_pk,'title': 'Attempted Update'}
        response = self.auth_client.patch(self.book_update_url, partial_payload, format='json')
        self.assertEqual(response.status_code, 403)