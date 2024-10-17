from fastapi import FastAPI, Request, HTTPException, Depends
from starlette.middleware.base import BaseHTTPMiddleware

from auth import TokenAuthMiddleware


app = FastAPI()

# Add middleware to the app
app.add_middleware(TokenAuthMiddleware)

# Dependency to extract the user info from the request state
def get_current_user(request: Request):
    if not hasattr(request.state, "user"):
        raise HTTPException(status_code=401, detail="User not authenticated")
    return request.state.user

# Root endpoint (no token required)
@app.get("/")
async def root(user: dict = Depends(get_current_user)):
    return {"message": "Hello!", "user": user}

