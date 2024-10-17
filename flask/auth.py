import os
import jwt
from jwt import PyJWKClient
from flask import request, g, abort

# OIDC Provider details (example using Auth0)
OIDC_ISSUER = os.getenv('APP_OIDC_ISSUER_URL')
OIDC_JWKS_URL = os.getenv('APP_OIDC_JWKS_URL')
OIDC_AUDIENCE = os.getenv('APP_OIDC_AUDIENCE')

# Fetch and cache JWKS (public keys)
jwks_client = PyJWKClient(OIDC_JWKS_URL)

def token_required(f):
    def decorator(*args, **kwargs):
        authorization = request.headers.get("Authorization")
        if authorization is None or not authorization.startswith("Bearer "):
            abort(403, description="Invalid or missing token")

        token = authorization[len("Bearer "):]  # Extract the token after "Bearer "
        
        try:
            # Verify and decode the token
            signing_key = jwks_client.get_signing_key_from_jwt(token)
            decoded_token = jwt.decode(
                token,
                signing_key.key,
                algorithms=["RS256"],
                audience=OIDC_AUDIENCE,
                issuer=OIDC_ISSUER
            )
        except jwt.ExpiredSignatureError:
            abort(401, description="Token has expired")
        except jwt.InvalidTokenError:
            abort(403, description="Invalid token")

        # Store the decoded token in the request context
        g.user = decoded_token

        return f(*args, **kwargs)
    
    decorator.__name__ = f.__name__  # Needed for Flask to recognize the decorator correctly
    return decorator
