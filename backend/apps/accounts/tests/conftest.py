import pytest
import jwt

from core.settings import SECRET_KEY


@pytest.fixture
def api_client():
    from rest_framework.test import APIClient

    return APIClient()


@pytest.fixture
def valid_token():
    """Fixture to provide a valid personal access token."""
    return "2d459c38db3fc0e211ab2deb157b1683339c013d"


@pytest.fixture
def invalid_token():
    """Fixture to provide an invalid personal access token."""
    return "invalid_personal_access_token"


@pytest.fixture
def expected_jwt_token(valid_token):
    """Fixture to provide the expected JWT token."""
    return jwt.encode(
        {"personal_access_token": valid_token}, SECRET_KEY, algorithm="HS256"
    )
