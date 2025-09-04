import os
import django

# Set up the Django environment.
# Replace 'your_project_name' with the actual name of your Django project.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project_name.settings')
django.setup()

# Import the models from your application.
from .models import Author, Book, Library, Librarian

def run_queries():
    """
    Executes a series of queries to demonstrate the relationships between the models.
    """
    # --- Step 1: Create sample data for the queries ---
    print("--- Creating sample data ---")
    
    # Create an Author instance
    author1 = Author.objects.create(name="George Orwell")
    
    # Create two Book instances and associate them with the author.
    book1 = Book.objects.create(title="1984", author=author1, publication_year=1949)
    book2 = Book.objects.create(title="Animal Farm", author=author1, publication_year=1945)

    # Create a Library and add the books to it.
    main_library = Library.objects.create(name="Main City Library")
    main_library.books.add(book1, book2)
    
    # Create a Librarian and associate them with the Library.
    librarian1 = Librarian.objects.create(name="Jane Doe", library=main_library)

    print("Sample data created successfully.\n")

    # --- Step 2: Perform the requested queries ---
    print("--- Executing queries ---")

    # Query 1: Query all books by a specific author.
    print(f"1. Querying all books by author: {author1.name}")
    books_by_author = Book.objects.filter(author=author1)
    if books_by_author.exists():
        for book in books_by_author:
            print(f"   - Found book: '{book.title}'")
    else:
        print("   - No books found for this author.")
    print("-" * 20)

    # Query 2: List all books in a library.
    print(f"2. Listing all books in the library: {main_library.name}")
    library_books = main_library.books.all()
    if library_books.exists():
        for book in library_books:
            print(f"   - Found book: '{book.title}'")
    else:
        print("   - No books found in this library.")
    print("-" * 20)

    # Query 3: Retrieve the librarian for a library.
    print(f"3. Retrieving the librarian for the library: {main_library.name}")
    try:
        library_librarian = main_library.librarian
        print(f"   - Found librarian: {library_librarian.name}")
    except Librarian.DoesNotExist:
        print("   - No librarian found for this library.")
    print("-" * 20)

if __name__ == '__main__':
    run_queries()
