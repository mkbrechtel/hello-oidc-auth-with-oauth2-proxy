import os
import jwt
from jwt import PyJWKClient
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, HTTPException
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

class TokenAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        authorization: str = request.headers.get("Authorization")
        if authorization is None or not authorization.startswith("Bearer "):
            raise HTTPException(status_code=403, detail="Invalid or missing token")
        token = authorization[len("Bearer "):]  # Extract the token after "Bearer "

        # Verify and decode the token
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
            raise HTTPException(status_code=401, detail="Token has expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=403, detail="Invalid token")

        # Store the decoded token in the request state
        request.state.user = decoded_token

        # Proceed to the next handler
        response = await call_next(request)
        return response
