import pytest
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
from django.test import RequestFactory
from rest_framework import status
from unittest.mock import patch, Mock
import jwt
from rest_framework.test import APIClient
from apps.cameras.views import CameraView
from core.settings import PERSONAL_ACCESS_TOKEN


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def access_token():
    access_token = PERSONAL_ACCESS_TOKEN

    encoded_token = jwt.encode(
        {"personal_access_token": access_token}, settings.SECRET_KEY, algorithm="HS256"
    )

    return encoded_token


@pytest.fixture
def authenticated_client(client, access_token):
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
    return client


@pytest.fixture
def factory():
    return RequestFactory()


@pytest.fixture
def personal_access_token(access_token):
    return access_token


@pytest.fixture
def valid_camera_data():
    return {
        "id": 112859,
        "name": "Street",
        "type": "h264",
        "snapshot": {
            "url": "https://d1bkj0vwu8cp7q.cloudfront.net/snapshot/112859/20240811-092930-352e4483-2dbd-4f88-bff2-8febf0b5cad5.jpg",
            "created_at": "2024-08-11T09:29:30Z",
        },
        "status": "online",
        "live_snapshot": "https://m3-eu8.angelcam.com/cameras/112859/snapshots/snapshot.jpg?token=eyJjYW1lcmFfaWQiOiIxMTI4NTkiLCJkZXZpY2VfaWQiOiIxMTI4NTkiLCJ0aW1lIjoxNzIzMzY5OTQ4MTA1MTM1LCJ0aW1lb3V0IjoxMjB9%2Ee10186ef8b504c9caa84e79724c91dadd6593d6f91758462d9d18e32dbd5d27d",
        "streams": [
            {
                "format": "mjpeg",
                "url": "https://m3-eu8.angelcam.com/cameras/112859/streams/mjpeg/stream.mjpeg?token=eyJjYW1lcmFfaWQiOiIxMTI4NTkiLCJkZXZpY2VfaWQiOiIxMTI4NTkiLCJ0aW1lIjoxNzIzMzY5OTQ4MTA1MjEzLCJ0aW1lb3V0IjoxMjB9%2E6c815854a096f1f42d4719b1000f8f6a6a80d215d8f74042c3536e84ed898e68",
            },
            {
                "format": "mp4",
                "url": "https://m3-eu8.angelcam.com/cameras/112859/streams/mp4/stream.mp4?token=eyJjYW1lcmFfaWQiOiIxMTI4NTkiLCJkZXZpY2VfaWQiOiIxMTI4NTkiLCJ0aW1lIjoxNzIzMzY5OTQ4MTA1MjQ2LCJ0aW1lb3V0IjoxMjB9%2E2d85546cad73d3bfe40473054d5f9379a3f604a6aff72228462c33f4967bf471",
            },
            {
                "format": "mpegts",
                "url": "https://m3-eu8.angelcam.com/cameras/112859/streams/mpegts/stream.ts?token=eyJjYW1lcmFfaWQiOiIxMTI4NTkiLCJkZXZpY2VfaWQiOiIxMTI4NTkiLCJ0aW1lIjoxNzIzMzY5OTQ4MTA1Mjc0LCJ0aW1lb3V0IjoxMjB9%2E6865c7cc19060a7564dac657897b5bbba2cb8d11c9fb6d1b59d182e494800783",
            },
            {
                "format": "hls",
                "url": "https://m3-eu8.angelcam.com/cameras/112859/streams/hls/playlist.m3u8?token=eyJjYW1lcmFfaWQiOiIxMTI4NTkiLCJkZXZpY2VfaWQiOiIxMTI4NTkiLCJ0aW1lIjoxNzIzMzY5OTQ4MTA1Mjk4LCJ0aW1lb3V0IjozNjAwfQ%3D%3D%2E7f427294285b5bcc86256a41c9b54ed8b08e261e0505978353e586d8a56528e1",
            },
        ],
        "applications": [{"code": "CRA"}],
        "owner": {
            "email": "hiring@angelcam.com",
            "first_name": "Angelcam",
            "last_name": "Hiring",
        },
        "has_recording": True,
        "has_notifications": False,
        "audio_enabled": True,
        "low_latency_enabled": True,
    }


@pytest.fixture
def valid_get_recording_info():
    return {
        "status": "READY",
        "retention": "P3D",
        "deactivated_at": None,
        "recording_start": "2024-08-08T01:09:12Z",
        "recording_end": "2024-08-11T10:09:39Z",
    }


@pytest.fixture
def valid_timeline_data():
    return {
        "start": "2024-08-09T01:09:12Z",
        "end": "2024-08-09T10:09:37Z",
        "segments": [
            {"start": "2024-08-09T01:09:12Z", "end": "2024-08-09T01:09:38Z"},
            {"start": "2024-08-09T01:37:38Z", "end": "2024-08-09T01:39:38Z"},
        ],
    }


@pytest.fixture
def valid_recording_stream_data():
    return {
        "format": "hls",
        "url": "https://e1-eu2.angelcam.com/recording/streams/770baf82-23fe-46cf-b4b5-6f1a5be00e4f/hls/playlist.m3u8",
        "stream_info": "https://api.angelcam.com/v1/recording/stream/e1-eu2.angelcam.com/770baf82-23fe-46cf-b4b5-6f1a5be00e4f/",
        "stream_controls": {
            "base_url": "https://e1-eu2.angelcam.com/recording/streams/770baf82-23fe-46cf-b4b5-6f1a5be00e4f/",
            "play": "https://e1-eu2.angelcam.com/recording/streams/770baf82-23fe-46cf-b4b5-6f1a5be00e4f/play/",
            "pause": "https://e1-eu2.angelcam.com/recording/streams/770baf82-23fe-46cf-b4b5-6f1a5be00e4f/pause/",
            "speed": "https://e1-eu2.angelcam.com/recording/streams/770baf82-23fe-46cf-b4b5-6f1a5be00e4f/speed/",
        },
    }


@pytest.fixture
def valid_camera_list_data():
    return {
        "count": 2,
        "next": None,
        "previous": None,
        "results": [
            {
                "id": 112860,
                "name": "Sample",
                "type": "mjpeg",
                "snapshot": {
                    "url": "https://d1bkj0vwu8cp7q.cloudfront.net/snapshot/112860/20240811-092414-d7342d2a-571e-46cd-b096-5ac73589dd44.jpg",
                    "created_at": "2024-08-11T09:24:14Z",
                },
                "status": "online",
                "live_snapshot": "https://m4-eu8.angelcam.com/cameras/112860/snapshots/snapshot.jpg?token=eyJjYW1lcmFfaWQiOiIxMTI4NjAiLCJkZXZpY2VfaWQiOiIxMTI4NjAiLCJ0aW1lIjoxNzIzMzY5NDU3MTA0MDM5LCJ0aW1lb3V0IjoxMjB9%2Eda72a32c13994739c2901cada3dc4b264bd7a09df6e127c5cff3ee4ae586fbf1",
                "streams": [
                    {
                        "format": "mjpeg",
                        "url": "https://m4-eu8.angelcam.com/cameras/112860/streams/mjpeg/stream.mjpeg?token=eyJjYW1lcmFfaWQiOiIxMTI4NjAiLCJkZXZpY2VfaWQiOiIxMTI4NjAiLCJ0aW1lIjoxNzIzMzY5NDU3MTA0MTE2LCJ0aW1lb3V0IjoxMjB9%2Ee06ff63b186a4f3903131dff6ae913fee71ab6c281a4bad25ed954c02389a238",
                    }
                ],
                "applications": [],
                "owner": {
                    "email": "hiring@angelcam.com",
                    "first_name": "Angelcam",
                    "last_name": "Hiring",
                },
                "has_recording": False,
                "has_notifications": False,
                "audio_enabled": True,
                "low_latency_enabled": True,
            },
            {
                "id": 112859,
                "name": "Street",
                "type": "h264",
                "snapshot": {
                    "url": "https://d1bkj0vwu8cp7q.cloudfront.net/snapshot/112859/20240811-092930-352e4483-2dbd-4f88-bff2-8febf0b5cad5.jpg",
                    "created_at": "2024-08-11T09:29:30Z",
                },
                "status": "online",
                "live_snapshot": "https://m3-eu8.angelcam.com/cameras/112859/snapshots/snapshot.jpg?token=eyJjYW1lcmFfaWQiOiIxMTI4NTkiLCJkZXZpY2VfaWQiOiIxMTI4NTkiLCJ0aW1lIjoxNzIzMzY5NDU3MTMzODY3LCJ0aW1lb3V0IjoxMjB9%2Efa3b083d1c6349abe62ecb1afea990cd62706ba744ee1d916c7ff78297bc348d",
                "streams": [
                    {
                        "format": "mjpeg",
                        "url": "https://m3-eu8.angelcam.com/cameras/112859/streams/mjpeg/stream.mjpeg?token=eyJjYW1lcmFfaWQiOiIxMTI4NTkiLCJkZXZpY2VfaWQiOiIxMTI4NTkiLCJ0aW1lIjoxNzIzMzY5NDU3MTMzOTM5LCJ0aW1lb3V0IjoxMjB9%2Eb6d4d6033313e0bcac075db73db585e9c0e5d109b241c0208c4346b2e7c3229c",
                    },
                    {
                        "format": "mp4",
                        "url": "https://m3-eu8.angelcam.com/cameras/112859/streams/mp4/stream.mp4?token=eyJjYW1lcmFfaWQiOiIxMTI4NTkiLCJkZXZpY2VfaWQiOiIxMTI4NTkiLCJ0aW1lIjoxNzIzMzY5NDU3MTMzOTczLCJ0aW1lb3V0IjoxMjB9%2E7b3c23986d0beaf39b6d9cc9e6e33831765033f6cf98041c5f9e0aba7a10e426",
                    },
                    {
                        "format": "mpegts",
                        "url": "https://m3-eu8.angelcam.com/cameras/112859/streams/mpegts/stream.ts?token=eyJjYW1lcmFfaWQiOiIxMTI4NTkiLCJkZXZpY2VfaWQiOiIxMTI4NTkiLCJ0aW1lIjoxNzIzMzY5NDU3MTM0MDAxLCJ0aW1lb3V0IjoxMjB9%2E8125a5d7cf38b6923e89ad075946a8c80d4ae5c69fa818a05634d840c9d07ac2",
                    },
                    {
                        "format": "hls",
                        "url": "https://m3-eu8.angelcam.com/cameras/112859/streams/hls/playlist.m3u8?token=eyJjYW1lcmFfaWQiOiIxMTI4NTkiLCJkZXZpY2VfaWQiOiIxMTI4NTkiLCJ0aW1lIjoxNzIzMzY5NDU3MTM0MDI2LCJ0aW1lb3V0IjozNjAwfQ%3D%3D%2E664ceb0ac3b9972abc576c5f8417f4844c18c6772aca77366e90166112477012",
                    },
                ],
                "applications": [{"code": "CRA"}],
                "owner": {
                    "email": "hiring@angelcam.com",
                    "first_name": "Angelcam",
                    "last_name": "Hiring",
                },
                "has_recording": True,
                "has_notifications": True,
                "audio_enabled": True,
                "low_latency_enabled": True,
            },
        ],
    }
