# cameras/urls.py
from django.urls import path
from .views import (
    CameraListView,
    CameraView,
    CamerasRecordingTimeLineView,
    StreamView,
    RecordingView,
    PlayRecordingView,
    PauseRecordingView,
    SpeedRecordingView,
)

urlpatterns = [
    path("cameras/", CameraListView.as_view(), name="camera-list"),
    path("camera/<int:camera_id>", CameraView.as_view(), name="camera"),
    path(
        "camera/<str:camera_id>/recording/timeline/",
        CamerasRecordingTimeLineView.as_view(),
        name="camera-recording-timeline",
    ),
    path(
        "camera/<str:camera_id>/recording/stream",
        StreamView.as_view(),
        name="camera-recording-stream",
    ),
    path(
        "camera/<str:camera_id>/recording/info",
        RecordingView.as_view(),
        name="camera-recording-info",
    ),
    path(
        "recording/<str:domain>/<str:stream_id>/play",
        PlayRecordingView.as_view(),
        name="play-recording",
    ),
    path(
        "recording/<str:domain>/<str:stream_id>/pause",
        PauseRecordingView.as_view(),
        name="pause-recording",
    ),
    path(
        "recording/<str:domain>/<str:stream_id>/speed",
        SpeedRecordingView.as_view(),
        name="speed-recording",
    ),
]
