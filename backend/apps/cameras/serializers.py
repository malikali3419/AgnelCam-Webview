from rest_framework import serializers


class SnapshotSerializer(serializers.Serializer):
    url = serializers.URLField()
    created_at = serializers.DateTimeField()


class StreamSerializer(serializers.Serializer):
    format = serializers.CharField(max_length=50)
    url = serializers.URLField()


class ApplicationSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=50)


class OwnerSerializer(serializers.Serializer):
    email = serializers.EmailField()
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)


class CameraSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=255)
    type = serializers.CharField(max_length=50)
    snapshot = SnapshotSerializer()
    status = serializers.CharField(max_length=50)
    live_snapshot = serializers.URLField()
    streams = StreamSerializer(many=True)
    applications = ApplicationSerializer(many=True, required=False)
    owner = OwnerSerializer()
    has_recording = serializers.BooleanField()
    has_notifications = serializers.BooleanField()
    audio_enabled = serializers.BooleanField()
    low_latency_enabled = serializers.BooleanField()


class CameraListResponseSerializer(serializers.Serializer):
    count = serializers.IntegerField()
    next = serializers.URLField(allow_null=True)
    previous = serializers.URLField(allow_null=True)
    results = CameraSerializer(many=True)


class SegmentSerializer(serializers.Serializer):
    start = serializers.DateTimeField()
    end = serializers.DateTimeField()


class RecordingSerializer(serializers.Serializer):
    status = serializers.CharField()
    retention = serializers.CharField()
    deactivated_at = serializers.DateTimeField(allow_null=True)
    recording_start = serializers.DateTimeField()
    recording_end = serializers.DateTimeField()


class TimelineSerializer(serializers.Serializer):
    start = serializers.DateTimeField()
    end = serializers.DateTimeField()
    segments = SegmentSerializer(many=True)


class StreamControlsSerializer(serializers.Serializer):
    base_url = serializers.URLField()
    play = serializers.URLField()
    pause = serializers.URLField()
    speed = serializers.URLField()


class StreamSerializer(serializers.Serializer):
    format = serializers.CharField()
    url = serializers.URLField()
    stream_info = serializers.URLField()
    stream_controls = StreamControlsSerializer()


class SpeedUpdateSerializer(serializers.Serializer):
    speed = serializers.FloatField()

    def validate_speed(self, value):
        if value < 0:
            raise serializers.ValidationError("Speed must be a non-negative value.")
        return value
