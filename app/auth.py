import jwt
from datetime import datetime, timedelta
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed, ParseError


def get_the_token_from_header(token):
    token = token.replace("Bearer", "").replace(" ", "")  # clean the token
    return token


def verify_user(authorization):
    """
    Verify a JWT token

    Args:
        authorization (str): An authorization header sent in request.

    Returns:
        payload (dict): decode info found in token.
    """

    # Extract the JWT from the Authorization header
    if authorization is None:
        return None

    # Decode the JWT and verify its signature
    try:
        token = get_the_token_from_header(authorization)
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    except jwt.exceptions.InvalidSignatureError:
        raise AuthenticationFailed("Invalid signature")
    except:
        raise ParseError()

    # return the token payload
    return payload


def sign_token(user):
    """
    Sign a JWT token

    Args:
        user (dict): user information to be decoded.

    Returns:
        jwt_token (str): encoded jwt token
    """
    # Create the JWT payload
    payload = {
        "user_id": user.id,
        "user_email": user.email,
        "exp": int(
            (
                datetime.now()
                + timedelta(hours=settings.JWT_CONF["TOKEN_LIFETIME_HOURS"])
            ).timestamp()
        ),
        "iat": datetime.now().timestamp(),
    }

    # Encode the JWT with your secret key
    jwt_token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

    return jwt_token
