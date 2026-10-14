"""Integration and API unit tests for User Service."""
from unittest.mock import AsyncMock, patch
from fastapi import status


def test_create_user_success(client):
    payload = {
        "first_name": "Alice",
        "last_name": "Smith",
        "email": "alice.smith@example.com",
        "age": 28,
        "address": "123 Main St, Tech City",
        "joining_date": "2026-01-15",
    }
    response = client.post("/api/v1/users", json=payload)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["id"] is not None
    assert data["first_name"] == "Alice"
    assert data["email"] == "alice.smith@example.com"
    # Registration must be False on creation
    assert data["is_registered"] is False


def test_create_user_duplicate_email(client):
    payload = {
        "first_name": "Bob",
        "last_name": "Builder",
        "email": "bob@example.com",
        "age": 35,
        "address": "456 Construction Rd",
    }
    response = client.post("/api/v1/users", json=payload)
    assert response.status_code == status.HTTP_201_CREATED

    # Attempt to create duplicate
    dup_response = client.post("/api/v1/users", json=payload)
    assert dup_response.status_code == status.HTTP_400_BAD_REQUEST
    assert "already exists" in dup_response.json()["detail"]


def test_register_user_endpoint(client):
    # Step 1: Create user (unregistered)
    payload = {
        "first_name": "Charlie",
        "last_name": "Brown",
        "email": "charlie@example.com",
        "age": 22,
        "address": "789 Pine St",
    }
    create_res = client.post("/api/v1/users", json=payload)
    user_id = create_res.json()["id"]
    assert create_res.json()["is_registered"] is False

    # Step 2: Dedicated registration endpoint
    reg_res = client.patch(f"/api/v1/users/{user_id}/register")
    assert reg_res.status_code == status.HTTP_200_OK
    assert reg_res.json()["is_registered"] is True

    # Check via GET endpoint
    get_res = client.get(f"/api/v1/users/{user_id}")
    assert get_res.status_code == status.HTTP_200_OK
    assert get_res.json()["is_registered"] is True


def test_update_user(client):
    create_res = client.post("/api/v1/users", json={
        "first_name": "Dave",
        "last_name": "Old",
        "email": "dave@example.com",
        "age": 40,
        "address": "Old Address",
    })
    user_id = create_res.json()["id"]

    update_payload = {
        "last_name": "New",
        "address": "New Address",
        "age": 41,
    }
    put_res = client.put(f"/api/v1/users/{user_id}", json=update_payload)
    assert put_res.status_code == status.HTTP_200_OK
    data = put_res.json()
    assert data["last_name"] == "New"
    assert data["address"] == "New Address"
    assert data["age"] == 41


def test_delete_user_cascades_poll_answers(client):
    create_res = client.post("/api/v1/users", json={
        "first_name": "Eve",
        "last_name": "Taylor",
        "email": "eve@example.com",
        "age": 30,
        "address": "Secret St",
    })
    user_id = create_res.json()["id"]

    with patch("app.services.poll_client.PollClient.delete_user_answers", new_callable=AsyncMock) as mock_delete:
        mock_delete.return_value = True

        del_res = client.delete(f"/api/v1/users/{user_id}")
        assert del_res.status_code == status.HTTP_204_NO_CONTENT
        mock_delete.assert_called_once_with(user_id)

    # Verify user is gone
    get_res = client.get(f"/api/v1/users/{user_id}")
    assert get_res.status_code == status.HTTP_404_NOT_FOUND
