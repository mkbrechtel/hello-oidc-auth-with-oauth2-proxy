import os
import jwt
from jwt import PyJWKClient
from flask import request, g, abort
import requests

if "OIDC_ISSUER_URL" in os.environ:
    OIDC_ISSUER_URL = os.getenv('OIDC_ISSUER_URL')
    print("OIDC_ISSUER_URL", OIDC_ISSUER_URL)

    OIDC_ISSUER_CONFIG_URL = f"{OIDC_ISSUER_URL}/.well-known/openid-configuration"
    OIDC_CONFIG = requests.get(OIDC_ISSUER_CONFIG_URL).json()
    print("OIDC_CONFIG",OIDC_CONFIG)

if "JWKS_URL" in os.environ:
    JWKS_URL = os.getenv('JWKS_URL')
else:
    JWKS_URL = OIDC_CONFIG["jwks_uri"]
print("JWKS_URL", JWKS_URL)

if "OAUTH_TOKEN_ISSUER" in os.environ:
    OAUTH_TOKEN_ISSUER = os.getenv('OAUTH_TOKEN_ISSUER')
else:
    OAUTH_TOKEN_ISSUER = OIDC_CONFIG["issuer"]
print("OAUTH_TOKEN_ISSUER",OAUTH_TOKEN_ISSUER)

OAUTH_TOKEN_AUDIENCE = os.getenv('OAUTH_TOKEN_AUDIENCE')
print("OAUTH_TOKEN_AUDIENCE", OAUTH_TOKEN_AUDIENCE)

if "OAUTH_TOKEN_JWT_ALGOS" in os.environ:
    OAUTH_TOKEN_JWT_ALGOS = os.getenv("OAUTH_TOKEN_JWT_ALGOS").split(",")
else:
    OAUTH_TOKEN_JWT_ALGOS = OIDC_CONFIG["id_token_signing_alg_values_supported"]
print("OAUTH_TOKEN_JWT_ALGOS",OAUTH_TOKEN_JWT_ALGOS)

jwks_client = PyJWKClient(JWKS_URL)

def token_required(f):
    def decorator(*args, **kwargs):
        authorization = request.headers.get("Authorization")
        if authorization is None or not authorization.startswith("Bearer "):
            abort(403, description="Invalid or missing token")

        token = authorization[len("Bearer "):]  # Extract the token after "Bearer "
        
        try:
            signing_key = jwks_client.get_signing_key_from_jwt(token)
            decoded_token = jwt.decode(
                token,
                signing_key.key,
                algorithms=OAUTH_TOKEN_JWT_ALGOS,
                audience=OAUTH_TOKEN_AUDIENCE,
                issuer=OAUTH_TOKEN_ISSUER
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
