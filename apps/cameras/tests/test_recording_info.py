import pytest
from unittest.mock import patch, Mock
from django.urls import reverse
from django.http import JsonResponse
from rest_framework import status
from apps.cameras.serializers import RecordingSerializer
from apps.cameras.views import RecordingView


@pytest.mark.django_db
@patch("requests.get")
def test_get_recording_info_success(
    mock_get, authenticated_client, valid_get_recording_info
):
    # Define mock response data
    mock_recording_data = valid_get_recording_info

    mock_response = Mock()
    mock_response.status_code = status.HTTP_200_OK
    mock_response.json.return_value = mock_recording_data
    mock_get.return_value = mock_response

    url = reverse("camera-recording-info", kwargs={"camera_id": "112859"})

    response = authenticated_client.get(url)

    serializer = RecordingSerializer(data=mock_recording_data)
    serializer.is_valid()

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == serializer.data


@pytest.mark.django_db
@patch("requests.get")
def test_get_recording_info_failure(mock_get, authenticated_client):
    mock_response = Mock()
    mock_response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    mock_response.json.return_value = {"detail": "Failed to retrieve recording data"}
    mock_get.return_value = mock_response

    url = reverse("camera-recording-info", kwargs={"camera_id": "112859"})

    response = authenticated_client.get(url)

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert response.json() == {"detail": "Failed to retrieve recording data"}


@pytest.mark.django_db
@patch("requests.get")
def test_get_recording_info_invalid_data(mock_get, authenticated_client):
    mock_recording_data = {"status": "INVALID", "unexpected_field": "value"}

    mock_response = Mock()
    mock_response.status_code = status.HTTP_200_OK
    mock_response.json.return_value = mock_recording_data
    mock_get.return_value = mock_response

    url = reverse("camera-recording-info", kwargs={"camera_id": "112859"})

    response = authenticated_client.get(url)

    serializer = RecordingSerializer(data=mock_recording_data)
    serializer.is_valid()

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == serializer.errors
