from django.utils.deprecation import MiddlewareMixin
import jwt
import logging
from django.conf import settings

SECRET_KEY = settings.SECRET_KEY
logger = logging.getLogger(__name__)


class DecodeTokenMiddleware(MiddlewareMixin):
    def process_request(self, request):
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
