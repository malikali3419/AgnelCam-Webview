import pytest
from unittest.mock import patch, Mock
from django.urls import reverse
from django.http import JsonResponse
from rest_framework import status
from apps.cameras.serializers import TimelineSerializer
from apps.cameras.views import CamerasRecordingTimeLineView


@pytest.mark.django_db
@patch("requests.get")
def test_get_recording_timeline_success(
    mock_get, authenticated_client, valid_timeline_data
):
    mock_timeline_data = valid_timeline_data

    mock_response = Mock()
    mock_response.status_code = status.HTTP_200_OK
    mock_response.json.return_value = mock_timeline_data
    mock_get.return_value = mock_response

    url = (
        reverse("camera-recording-timeline", kwargs={"camera_id": "112859"})
        + "?start=2024-08-09T00:00:00Z&end=2024-08-09T23:59:59Z"
    )

    response = authenticated_client.get(url)

    serializer = TimelineSerializer(data=mock_timeline_data)
    serializer.is_valid()

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == serializer.data


@pytest.mark.django_db
@patch("requests.get")
def test_get_recording_timeline_missing_params(mock_get, authenticated_client):
    url = reverse("camera-recording-timeline", kwargs={"camera_id": "112859"})

    response = authenticated_client.get(url)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail": "Start and end parameters are required."}


@pytest.mark.django_db
@patch("requests.get")
def test_get_recording_timeline_invalid_data(mock_get, authenticated_client):
    mock_timeline_data = {"start": "INVALID", "end": "INVALID", "segments": "INVALID"}

    mock_response = Mock()
    mock_response.status_code = status.HTTP_200_OK
    mock_response.json.return_value = mock_timeline_data
    mock_get.return_value = mock_response

    url = (
        reverse("camera-recording-timeline", kwargs={"camera_id": "112859"})
        + "?start=2024-08-09T00:00:00Z&end=2024-08-09T23:59:59Z"
    )

    response = authenticated_client.get(url)

    serializer = TimelineSerializer(data=mock_timeline_data)
    serializer.is_valid()

    # Assertions
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == serializer.errors


@pytest.mark.django_db
@patch("requests.get")
def test_get_recording_timeline_failure(mock_get, authenticated_client):
    mock_response = Mock()
    mock_response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    mock_response.json.return_value = {"detail": "Failed to retrieve timeline data"}
    mock_get.return_value = mock_response

    url = (
        reverse("camera-recording-timeline", kwargs={"camera_id": "112859"})
        + "?start=2024-08-09T00:00:00Z&end=2024-08-09T23:59:59Z"
    )

    response = authenticated_client.get(url)

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert response.json() == {"detail": "Failed to retrieve timeline data"}
