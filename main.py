from fastapi import FastAPI, Header, HTTPException, Request
from pydantic import BaseModel
import jwt
from datetime import datetime, timedelta
from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

app = FastAPI()

# Initialize Limiter
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

# Secret key for JWT encoding/decoding
SECRET_KEY = "mysecretkey"

# Sample items dictionary
items = {
    "john@gmail.com": "jklmnb123",
    "root@hotmail.com": "pass123wd",
    "alperen@outlook.com": "strngpasswd02",
    "user@gmail.com": "zxcvb0123",
    "admin@gmail.com": "adminpasswd123"
}


# Model for JWT Token response
class TokenResponse(BaseModel):
    token: str


# Function to create a JWT
def create_jwt_token(name: str) -> str:
    expiration = datetime.now() + timedelta(hours=1)
    payload = {"sub": name, "exp": expiration}
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token


@app.get("/token/{name}", response_model=TokenResponse)
def get_token(name: str):
    token = create_jwt_token(name)
    return TokenResponse(token=token)


@app.get("/accounts/unsafe")
def get_items_unsafe():
    # Return items without any authentication
    return items


@app.get("/accounts/safe")
@limiter.limit("5/minute")  # Limit to 5 requests per minute per client
def get_items_safe(request: Request, authorization: str = Header(None)):
    if authorization is None:
        raise HTTPException(status_code=401, detail="Invalid token")

    # Extract the token from the header
    token = authorization.split(" ")[-1]

    try:
        # Decode the token to verify its validity
        jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return items
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


# Custom error handler for rate limit exceeded
@app.exception_handler(RateLimitExceeded)
async def rate_limit_error(request: Request, exc: RateLimitExceeded):
    raise HTTPException(status_code=429, detail="Rate limit exceeded. Try again later.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
