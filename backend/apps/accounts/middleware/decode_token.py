from django.utils.deprecation import MiddlewareMixin
import jwt
import logging
from django.conf import settings

SECRET_KEY = settings.SECRET_KEY
logger = logging.getLogger(__name__)


class DecodeTokenMiddleware(MiddlewareMixin):
    """
    Middleware to decode JWT tokens from the Authorization header and attach the decoded
    Personal Access Token to the request object.

    This middleware looks for a JWT in the Authorization header of incoming requests,
    decodes the token using the secret key, and extracts the Personal Access Token.
    It logs warnings for expired or invalid tokens and errors for unexpected issues.

    Request Header:
        - Authorization (str): The JWT token prefixed with "Bearer ".

    Request Attributes:
        - personal_access_token (str): The decoded Personal Access Token, if available.
    """

    def process_request(self, request):
        """
        Process the incoming request to decode the JWT token and attach the Personal Access Token.

        Extracts the JWT from the Authorization header, decodes it using the secret key,
        and attaches the Personal Access Token to the request object. Logs warnings for
        expired or invalid tokens and errors for unexpected issues.

        Parameters:
            - request (HttpRequest): The incoming HTTP request object.

        Returns:
            - None: This method does not modify the response; it just updates the request object.
        """
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return None

        if auth_header.startswith("Bearer "):
            app_token = auth_header.split("Bearer ")[1]
        else:
            app_token = auth_header

        try:
            decoded_data = jwt.decode(app_token, SECRET_KEY, algorithms=["HS256"])
            request.personal_access_token = decoded_data.get("personal_access_token")
        except jwt.ExpiredSignatureError:
            logger.warning("Expired token")
            return None
        except jwt.InvalidTokenError:
            logger.warning("Invalid token")
            return None
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return None
