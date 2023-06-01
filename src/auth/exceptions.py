from fastapi import HTTPException
from starlette import status

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


class InvalidCredentialsException(Exception):
    message = "Invalid credentials were provided"

    def __str__(self):
        return InvalidCredentialsException.message
