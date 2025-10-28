import pytest

@pytest.mark.django_db
def test_get_non_existing_book(api_client):
    response = api_client.get("/api/v1/books/9999/")
    assert response.status_code == 404

@pytest.mark.django_db
def test_create_book_without_title(api_client, sample_data):
    payload = {
        "description": "Adventure",
        "price": 19.99,
        "stock": 5,
        "publisher": sample_data["publisher"].id,
        "authors": [sample_data["author"].id]
    }
    response = api_client.post("/api/v1/books/", payload, format="json")
    assert response.status_code == 400

@pytest.mark.django_db
def test_update_non_existing_book(api_client):
    response = api_client.patch("/api/v1/books/9999/", {"price": 30.00}, format="json")
    assert response.status_code == 404

@pytest.mark.django_db
def test_delete_non_existing_book(api_client):
    response = api_client.delete("/api/v1/books/9999/")
    assert response.status_code == 404
