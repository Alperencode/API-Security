# API Security
This project demonstrates basic API security concepts in Python using FastAPI. It's used for collage presentation as an example.

## Key Features:
* JSON Web Token (JWT): Secure API access by generating and verifying JWTs for authentication.
* Rate Limiting: Implement request limits to protect against abuse and excessive usage.
Usage:
* Generate JWT Token: Endpoint to create a JWT for a user.
* Unsafe Items Endpoint: Retrieve items without authentication.
* Safe Items Endpoint: Access items only with a valid JWT and rate-limited requests.