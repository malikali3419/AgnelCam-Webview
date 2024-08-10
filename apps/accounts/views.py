from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import jwt
import requests
from core.settings import SECRET_KEY
from rest_framework.permissions import AllowAny
from .serializers import LoginSerializer


class LoginView(APIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        personal_access_token = serializer.validated_data["personal_access_token"]
        headers = {"Authorization": f"PersonalAccessToken {personal_access_token}"}
        response = requests.get("https://api.angelcam.com/v1/me/", headers=headers)
        if response.status_code != 200:
            return Response(
                {"error": "Invalid Personal Access Token"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        app_token = jwt.encode(
            {"personal_access_token": personal_access_token},
            SECRET_KEY,
            algorithm="HS256",
        )

        return Response({"token": app_token}, status=status.HTTP_200_OK)
