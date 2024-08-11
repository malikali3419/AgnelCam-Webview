import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from unittest.mock import patch
import jwt
from django.conf import settings

SECRET_KEY = settings.SECRET_KEY


@pytest.mark.django_db
@patch("requests.get")
def test_login_with_valid_token(mock_get, api_client, valid_token, expected_jwt_token):
    """Test login with a valid personal access token."""
    mock_get.return_value.status_code = 200
    url = reverse("login")

    response = api_client.post(
        url, {"personal_access_token": valid_token}, format="json"
    )

    assert response.status_code == status.HTTP_200_OK
    assert "token" in response.data
    assert response.data["token"] == expected_jwt_token


@pytest.mark.django_db
@patch("requests.get")
def test_login_with_invalid_token(mock_get, api_client, invalid_token):
    """Test login with an invalid personal access token."""
    mock_get.return_value.status_code = 401
    url = reverse("login")

    response = api_client.post(url, {"personal_access_token": invalid_token})

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "error" in response.data
    assert response.data["error"] == "Invalid Personal Access Token"


@pytest.mark.django_db
def test_login_with_invalid_data(api_client):
    """Test login with invalid data (e.g., missing token)."""
    url = reverse("login")

    response = api_client.post(url, {})

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "personal_access_token" in response.data
