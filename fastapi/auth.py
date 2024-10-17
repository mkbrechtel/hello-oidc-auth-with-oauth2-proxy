import os
import jwt
from jwt import PyJWKClient
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, HTTPException

# OIDC Provider details (example using Auth0)
OIDC_ISSUER = os.getenv('APP_OIDC_ISSUER_URL')
OIDC_JWKS_URL = os.getenv('APP_OIDC_JWKS_URL')
OIDC_AUDIENCE = os.getenv('APP_OIDC_AUDIENCE')

print(OIDC_ISSUER,OIDC_JWKS_URL,OIDC_AUDIENCE)
class TokenAuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        # Fetch and cache JWKS (public keys)
        self.jwks_client = PyJWKClient(OIDC_JWKS_URL)

    async def dispatch(self, request: Request, call_next):
        authorization: str = request.headers.get("Authorization")
        if authorization is None or not authorization.startswith("Bearer "):
            raise HTTPException(status_code=403, detail="Invalid or missing token")
        
        token = authorization[len("Bearer "):]  # Extract the token after "Bearer "

        # Verify and decode the token
        try:
            signing_key = self.jwks_client.get_signing_key_from_jwt(token)
            decoded_token = jwt.decode(
                token,
                signing_key.key,
                algorithms=["RS256"],
                audience=OIDC_AUDIENCE,
                issuer=OIDC_ISSUER
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
