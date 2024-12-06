from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
import jwt
from datetime import datetime, timedelta

app = FastAPI()

# Secret key for JWT encoding/decoding
SECRET_KEY = "mysecretkey"

# Sample items dictionary
items = {
    "apple": "A sweet red fruit.",
    "banana": "A yellow tropical fruit.",
    "carrot": "A crunchy orange vegetable.",
    "book": "A collection of written words.",
    "laptop": "A portable personal computer."
}


# Model for JWT Token response
class TokenResponse(BaseModel):
    token: str


# Function to create a JWT
def create_jwt_token(name: str) -> str:
    expiration = datetime.utcnow() + timedelta(hours=1)
    payload = {"sub": name, "exp": expiration}
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token


@app.get("/token/{name}", response_model=TokenResponse)
def get_token(name: str):
    token = create_jwt_token(name)
    return TokenResponse(token=token)


@app.get("/items/unsafe")
def get_items_unsafe():
    # Return items without any authentication
    return items


@app.get("/items/safe")
def get_items_safe(authorization: str = Header(None)):
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


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
