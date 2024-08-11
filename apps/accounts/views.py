from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import jwt
import requests
from core.settings import SECRET_KEY
from rest_framework.permissions import AllowAny
from .serializers import LoginSerializer


class LoginView(APIView):
    """
    View to handle user login by validating the Personal Access Token and issuing a JWT.

    Endpoint:
        POST /login/

    Request Body:
        - personal_access_token (str): The Personal Access Token for authentication.

    Response:
        - 200 OK: Returns a JSON response containing the JWT if the token is valid.
        - 400 Bad Request: If the request data is invalid.
        - 401 Unauthorized: If the Personal Access Token is invalid or not authenticated.
    """

    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        """
        Handle POST requests to authenticate a user and issue a JWT.

        Validates the incoming Personal Access Token, checks its authenticity, and generates a JWT if the token is valid.

        Parameters:
            - request (Request): The HTTP request object containing the Personal Access Token.

        Returns:
            - Response: A response object containing the JWT if authentication is successful or error messages if not.
        """
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
