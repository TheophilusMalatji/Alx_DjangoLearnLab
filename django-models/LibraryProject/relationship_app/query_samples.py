import os
import django

from .models import Author, Book, Library, Librarian


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()



def run_queries():
           
    
    author1 = Author.objects.create(name="George Orwell")
    book1 = Book.objects.create(title="1984", author=author1, publication_year=1949)
    book2 = Book.objects.create(title="Animal Farm", author=author1, publication_year=1945)
    books = [book1,book2]

    library_name = Library.objects.create(name="Main City Library")
    library_name.books.add(book1, book2)   
 
    librarian1 = Librarian.objects.create(name="Jane Doe", library=library_name)


    print("--- Executing queries ---")

    # Query all books by a specific author.
    print(f"1. Querying all books by author: {author1.name}")
    books_by_author = Book.objects.filter(author=author1)
    if books_by_author.exists():
        for book in books_by_author:
            print(f"   - Found book: '{book.title}'")
    else:
        print("   - No books found for this author.")
    print("-" * 20)

    # List all books in a library.
    #"Author.objects.get(name=author_name)", "objects.filter(author=author)
    print(f"2. Listing all books in the library: {library_name.name}")
    library_books = Library.objects.get(name=library_name.name)
    
    if library_books.exists():
        for book in library_books:
            print(f"   - Found book: '{book.title}'")
    else:
        print("   - No books found in this library.")
    print("-" * 20)
    #Retrieve the librarian for a library.
    #"Library.objects.get(name=library_name)", "books.all()
    #Librarian.objects.get(library=
    print(f"3. Retrieving the librarian for the library: {library_name.name}")
    try:
        library_librarian = library_name.librarian
        print(f"   - Found librarian: {library_librarian.name}")
    except Librarian.DoesNotExist:
        print("   - No librarian found for this library.")
    print("-" * 20)

if __name__ == '__main__':
    run_queries()
