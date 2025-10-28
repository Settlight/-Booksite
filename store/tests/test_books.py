import pytest

@pytest.mark.django_db
def test_get_books(api_client, sample_data):
    response = api_client.get("/api/v1/books/")
    assert response.status_code == 200
    assert any(b["title"] == "Harry Potter" for b in response.json())

@pytest.mark.django_db
def test_create_book(api_client, sample_data):
    payload = {
        "title": "The Hobbit",
        "description": "Adventure",
        "price": 19.99,
        "stock": 5,
        "publisher": sample_data["publisher"].id,
        "authors": [sample_data["author"].id]
    }
    response = api_client.post("/api/v1/books/", payload, format="json")
    assert response.status_code == 201
    assert response.json()["title"] == "The Hobbit"

@pytest.mark.django_db
def test_update_book(api_client, sample_data):
    book_id = sample_data["book"].id
    response = api_client.patch(f"/api/v1/books/{book_id}/", {"price": 30.00}, format="json")
    assert response.status_code == 200
    assert response.json()["price"] == "30.00"

@pytest.mark.django_db
def test_delete_book(api_client, sample_data):
    book_id = sample_data["book"].id
    response = api_client.delete(f"/api/v1/books/{book_id}/")
    assert response.status_code == 204
