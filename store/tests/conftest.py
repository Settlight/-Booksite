import pytest
from rest_framework.test import APIClient
from store.models import Author, Publisher, Book

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def sample_data(db):
    publisher = Publisher.objects.create(name="Test Publisher")
    author = Author.objects.create(name="Test Author")
    book = Book.objects.create(
        title="Harry Potter",
        description="Magic",
        publisher=publisher,
        price=10.99,
        stock=3
    )
    book.authors.add(author)
    return {"publisher": publisher, "author": author, "book": book}
