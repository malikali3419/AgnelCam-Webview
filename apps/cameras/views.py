import json

from django.http import JsonResponse, HttpResponseBadRequest
import requests
from django.views import View
from rest_framework import status
from .serializers import (
    CameraListResponseSerializer,
    CameraSerializer,
    TimelineSerializer,
    StreamSerializer,
    RecordingSerializer,
    SpeedUpdateSerializer,
)
from django.utils.decorators import method_decorator
from apps.utils.auth import require_personal_access_token


class CameraLiveStreamView(View):
    """
    View to retrieve the live stream URL for a given camera.

    Endpoint:
        GET /camera/<camera_id>/recording/stream

    Parameters:
        - camera_id (str): The unique identifier for the camera.

    Response:
        - 200 OK: Returns a JSON response containing the live stream URL.
        - 400 Bad Request: If unable to fetch the live stream URL.
    """

    @staticmethod
    def get(request, camera_id):
        headers = {
            "Authorization": f"PersonalAccessToken 01795484f0d844bc00c1be2e932de0541fa7f460"
        }
        response = requests.get(
            f"https://api.angelcam.com/v1/shared-cameras/{camera_id}/recording/stream/",
            headers=headers,
        )
        if response.status_code == 200:
            live_stream_url = response.json().get("live_stream_url")
            return JsonResponse({"live_stream_url": live_stream_url})
        else:
            return HttpResponseBadRequest("Unable to fetch live stream URL")


@method_decorator(require_personal_access_token, name="dispatch")
class CameraListView(View):
    """
    View to list all cameras for the authenticated user.

    Endpoint:
        GET /camera/

    Response:
        - 200 OK: Returns a JSON response containing a list of cameras.
        - 400 Bad Request: If there is an issue with the response data.
    """

    @staticmethod
    def get(request):
        headers = {
            "Authorization": f"PersonalAccessToken {request.personal_access_token}"
        }
        response = requests.get(
            "https://api.angelcam.com/v1/shared-cameras/", headers=headers
        )
        if response.status_code == 200:
            cameras_data = response.json()
            serializer = CameraListResponseSerializer(data=cameras_data)
            if serializer.is_valid():
                return JsonResponse(
                    serializer.data, safe=False, status=status.HTTP_200_OK
                )
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(require_personal_access_token, name="dispatch")
class CameraView(View):
    """
    View to retrieve details for a specific camera.

    Endpoint:
        GET /camera/<camera_id>/

    Parameters:
        - camera_id (str): The unique identifier for the camera.

    Response:
        - 200 OK: Returns a JSON response containing the camera details.
        - 400 Bad Request: If there is an issue with the response data.
    """

    @staticmethod
    def get(request, camera_id):
        headers = {
            "Authorization": f"PersonalAccessToken {request.personal_access_token}"
        }
        response = requests.get(
            f"https://api.angelcam.com/v1/shared-cameras/{camera_id}/", headers=headers
        )
        if response.status_code == 200:
            cameras_data = response.json()
            streams = cameras_data.get("streams", [])

            filtered_streams = [
                stream
                for stream in streams
                if stream.get("format") == "mjpeg" or stream.get("format") == "mp4"
            ]

            cameras_data["streams"] = filtered_streams

            serializer = CameraSerializer(data=cameras_data)
            if serializer.is_valid():
                return JsonResponse(
                    serializer.data, safe=False, status=status.HTTP_200_OK
                )
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse(
            {"error": "Failed to fetch camera data from external service"},
            status=status.HTTP_400_BAD_REQUEST,
        )


@method_decorator(require_personal_access_token, name="dispatch")
class CamerasRecordingTimeLineView(View):
    """
    View to retrieve the recording timeline for a specific camera.

    Endpoint:
        GET /camera/<camera_id>/recording/timeline/

    Parameters:
        - start (str): The start timestamp for the timeline.
        - end (str): The end timestamp for the timeline.

    Response:
        - 200 OK: Returns a JSON response containing the recording timeline data.
        - 400 Bad Request: If start or end parameters are missing or if there is an issue with the response data.
    """

    @staticmethod
    def get(request, camera_id):
        start = request.GET.get("start")
        end = request.GET.get("end")

        if not start or not end:
            return JsonResponse(
                {"detail": "Start and end parameters are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        headers = {
            "Authorization": f"PersonalAccessToken {request.personal_access_token}"
        }
        params = {"start": start, "end": end}
        response = requests.get(
            f"https://api.angelcam.com/v1/shared-cameras/{camera_id}/recording/timeline/",
            headers=headers,
            params=params,
        )
        if response.status_code == 200:
            timeline_data = response.json()
            serializer = TimelineSerializer(data=timeline_data)
            if serializer.is_valid():
                return JsonResponse(
                    serializer.data, safe=False, status=status.HTTP_200_OK
                )
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse(
            {"detail": "Failed to retrieve timeline data"}, status=response.status_code
        )


@method_decorator(require_personal_access_token, name="dispatch")
class StreamView(View):
    """
    View to retrieve the streaming data for a specific camera.

    Endpoint:
        GET /camera/<camera_id>/recording/stream/

    Parameters:
        - start (str): The start timestamp for the stream.

    Response:
        - 200 OK: Returns a JSON response containing the stream data.
        - 400 Bad Request: If start parameter is missing or if there is an issue with the response data.
    """

    @staticmethod
    def get(request, camera_id):
        start = request.GET.get("start")

        if not start:
            return JsonResponse(
                {"detail": "Start parameter is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        headers = {
            "Authorization": f"PersonalAccessToken {request.personal_access_token}"
        }
        params = {
            "start": start,
        }
        response = requests.get(
            f"https://api.angelcam.com/v1/shared-cameras/{camera_id}/recording/stream/",
            headers=headers,
            params=params,
        )
        if response.status_code == 200:
            stream_data = response.json()
            serializer = StreamSerializer(data=stream_data)
            if serializer.is_valid():
                return JsonResponse(
                    serializer.data, safe=False, status=status.HTTP_200_OK
                )
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse(
            {"detail": "Failed to retrieve stream data"}, status=response.status_code
        )


@method_decorator(require_personal_access_token, name="dispatch")
class RecordingView(View):
    """
    View to retrieve recording data for a specific camera.

    Endpoint:
        GET /camera/<camera_id>/recording/

    Parameters:
        - camera_id (str): The unique identifier for the camera.

    Response:
        - 200 OK: Returns a JSON response containing the recording data.
        - 400 Bad Request: If there is an issue with the response data.
    """

    @staticmethod
    def get(request, camera_id):
        headers = {
            "Authorization": f"PersonalAccessToken {request.personal_access_token}"
        }

        response = requests.get(
            f"https://api.angelcam.com/v1/shared-cameras/{camera_id}/recording/",
            headers=headers,
        )
        if response.status_code == 200:
            recording_data = response.json()
            serializer = RecordingSerializer(data=recording_data)
            if serializer.is_valid():
                return JsonResponse(
                    serializer.data, safe=False, status=status.HTTP_200_OK
                )
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse(
            {"detail": "Failed to retrieve recording data"}, status=response.status_code
        )


@method_decorator(require_personal_access_token, name="dispatch")
class PlayRecordingView(View):
    """
    View to start playback of a recording for a specific camera.

    Endpoint:
        POST /camera/<domain>/recording/streams/<stream_id>/play/

    Parameters:
        - domain (str): The domain of the recording service.
        - stream_id (str): The unique identifier for the stream.

    Response:
        - 200 OK: Returns a JSON response indicating that playback has started.
        - 400 Bad Request: If playback cannot be started or if there is an issue with the request.
    """

    @staticmethod
    def get(request, domain, stream_id):
        headers = {
            "Authorization": f"PersonalAccessToken {request.personal_access_token}"
        }

        response = requests.post(
            f"https://{domain}/recording/streams/{stream_id}/play/",
            headers=headers,
        )
        if response.status_code == 204:
            return JsonResponse(
                {"status": "playing"}, safe=False, status=status.HTTP_200_OK
            )
        return JsonResponse(
            {"detail": "Failed to play the recording"}, status=response.status_code
        )


@method_decorator(require_personal_access_token, name="dispatch")
class PauseRecordingView(View):
    """
    View to pause playback of a recording for a specific camera.

    Endpoint:
        POST /camera/<domain>/recording/streams/<stream_id>/pause/

    Parameters:
        - domain (str): The domain of the recording service.
        - stream_id (str): The unique identifier for the stream.

    Response:
        - 200 OK: Returns a JSON response indicating that playback has been paused.
        - 400 Bad Request: If playback cannot be paused or if there is an issue with the request.
    """

    @staticmethod
    def get(request, domain, stream_id):
        headers = {
            "Authorization": f"PersonalAccessToken {request.personal_access_token}"
        }

        response = requests.post(
            f"https://{domain}/recording/streams/{stream_id}/pause/",
            headers=headers,
        )
        if response.status_code == 204:
            return JsonResponse(
                {"status": "paused"}, safe=False, status=status.HTTP_200_OK
            )
        return JsonResponse(
            {"detail": "Failed to pause the recording"}, status=response.status_code
        )


@method_decorator(require_personal_access_token, name="dispatch")
class SpeedRecordingView(View):
    """
    View to update the playback speed of a recording for a specific camera.

    Endpoint:
        POST /camera/<domain>/recording/streams/<stream_id>/speed/

    Parameters:
        - domain (str): The domain of the recording service.
        - stream_id (str): The unique identifier for the stream.

    Request Body:
        - speed (int): The playback speed.

    Response:
        - 200 OK: Returns a JSON response indicating that the speed has been updated.
        - 400 Bad Request: If there is an issue with the request or if the speed value is invalid.
    """

    @staticmethod
    def get(request, domain, stream_id):
        try:
            data = request.body
            json_data = json.loads(data)
        except ValueError:
            return JsonResponse(
                {"detail": "Invalid JSON"}, status=status.HTTP_400_BAD_REQUEST
            )

        serializer = SpeedUpdateSerializer(data=json_data)
        if not serializer.is_valid():
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data
        speed = int(validated_data["speed"])
        headers = {
            "Authorization": f"PersonalAccessToken {request.personal_access_token}"
        }

        data = {"speed": speed}

        response = requests.get(
            f"https://{domain}/recording/streams/{stream_id}/speed/",
            headers=headers,
            json=data,
        )
        if response.status_code == 200:
            return JsonResponse(
                {"success": "true"}, safe=False, status=status.HTTP_200_OK
            )
        return JsonResponse(
            {"detail": "Failed to update the playback speed"},
            status=response.status_code,
        )
