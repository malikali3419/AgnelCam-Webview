import pytest
import requests
from django.urls import reverse
from rest_framework import status
from unittest.mock import patch
from rest_framework.test import APIClient
from apps.cameras.views import CameraView
from unittest.mock import patch, Mock
from apps.cameras.serializers import CameraSerializer
from django.http import JsonResponse


@pytest.mark.django_db
@patch("requests.get")
def test_get_camera_data_success(mock_get, authenticated_client, valid_camera_data):
    url = reverse("camera", kwargs={"camera_id": 112859})
    mock_get.return_value = Mock(status_code=200, json=lambda: valid_camera_data)
    response = authenticated_client.get(url)
    serializer = CameraSerializer(data=valid_camera_data)
    serializer.is_valid()
    expected_data = serializer.data
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == expected_data


@patch("requests.get")
def test_get_camera_data_invalid_data(mock_requests, authenticated_client):
    url = reverse("camera", kwargs={"camera_id": 112859})
    mock_response = mock_requests.return_value
    mock_response.status_code = status.HTTP_400_BAD_REQUEST

    response = authenticated_client.get(url)

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@patch("requests.get")
def test_get_camera_data_unauthorized(mock_requests, authenticated_client):
    url = reverse("camera", kwargs={"camera_id": 112859})

    mock_response = mock_requests.return_value
    mock_response.status_code = status.HTTP_401_UNAUTHORIZED
    authenticated_client.credentials()

    response = authenticated_client.get(url)
    print(response, "RESPONSE")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
