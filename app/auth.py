import jwt
from datetime import datetime, timedelta
from django.conf import settings


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
        # clean the token
        token = authorization.replace("Bearer", "").replace(" ", "")
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms="HS256",
            options={"verify_signature": False},
        )
    except:
        print("Invalid")
        return None

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
