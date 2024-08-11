import pytest
from unittest.mock import patch, Mock
from django.urls import reverse
from rest_framework import status
from apps.cameras.serializers import StreamSerializer
from apps.cameras.views import StreamView


@pytest.mark.django_db
@patch("requests.get")
def test_get_stream_success(
    mock_get, authenticated_client, valid_recording_stream_data
):
    mock_stream_data = valid_recording_stream_data
    mock_response = Mock()
    mock_response.status_code = status.HTTP_200_OK
    mock_response.json.return_value = mock_stream_data
    mock_get.return_value = mock_response

    url = (
        reverse("camera-recording-stream", kwargs={"camera_id": "112859"})
        + "?start=2024-08-09T00:00:00Z"
    )

    response = authenticated_client.get(url)

    serializer = StreamSerializer(data=mock_stream_data)
    serializer.is_valid()

    # Assertions
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == serializer.data


@pytest.mark.django_db
@patch("requests.get")
def test_get_stream_missing_param(mock_get, authenticated_client):
    url = reverse("camera-recording-stream", kwargs={"camera_id": "112859"})

    response = authenticated_client.get(url)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail": "Start parameter is required."}


@pytest.mark.django_db
@patch("requests.get")
def test_get_stream_invalid_data(mock_get, authenticated_client):
    mock_stream_data = {
        "format": "INVALID",
        "url": "INVALID",
        "stream_info": "INVALID",
        "stream_controls": "INVALID",
    }

    # Setup the mock response
    mock_response = Mock()
    mock_response.status_code = status.HTTP_200_OK
    mock_response.json.return_value = mock_stream_data
    mock_get.return_value = mock_response

    url = (
        reverse("camera-recording-stream", kwargs={"camera_id": "112859"})
        + "?start=2024-08-09T00:00:00Z"
    )

    response = authenticated_client.get(url)

    serializer = StreamSerializer(data=mock_stream_data)
    serializer.is_valid()

    # Assertions
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == serializer.errors


@pytest.mark.django_db
@patch("requests.get")
def test_get_stream_failure(mock_get, authenticated_client):
    mock_response = Mock()
    mock_response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    mock_response.json.return_value = {"detail": "Failed to retrieve stream data"}
    mock_get.return_value = mock_response

    url = (
        reverse("camera-recording-stream", kwargs={"camera_id": "112859"})
        + "?start=2024-08-09T00:00:00Z"
    )

    response = authenticated_client.get(url)

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert response.json() == {"detail": "Failed to retrieve stream data"}
