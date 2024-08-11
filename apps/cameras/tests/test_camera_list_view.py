import pytest
from django.urls import reverse
from rest_framework import status
from unittest.mock import patch
from rest_framework.test import APIClient


@pytest.mark.django_db
@patch("apps.cameras.views.requests.get")
def test_get_camera_list_success(
    mock_requests, authenticated_client, valid_camera_list_data
):
    url = reverse("camera-list")

    mock_response = mock_requests.return_value
    mock_response.status_code = status.HTTP_200_OK
    mock_response.json.return_value = valid_camera_list_data

    response = authenticated_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == mock_response.json.return_value


@pytest.mark.django_db
@patch("apps.cameras.views.requests.get")
def test_get_camera_list_auth_failure(mock_requests, authenticated_client):
    url = reverse("camera-list")

    mock_response = mock_requests.return_value
    mock_response.status_code = status.HTTP_401_UNAUTHORIZED

    authenticated_client.credentials()

    response = authenticated_client.get(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"error": "Unauthorized"}
