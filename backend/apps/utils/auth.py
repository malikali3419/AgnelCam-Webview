from functools import wraps
from django.http import JsonResponse
from rest_framework import status


def require_personal_access_token(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not hasattr(request, "personal_access_token"):
            return JsonResponse(
                {"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED
            )
        return view_func(request, *args, **kwargs)

    return _wrapped_view
