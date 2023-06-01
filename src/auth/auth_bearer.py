from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt, JWTError
from starlette.authentication import AuthenticationBackend
from starlette.requests import Request

from src.settings import Settings, settings


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        """
        Class represents JWT Bearer Auth for fastapi
        :param auto_error: Call exception after not valid token
        """
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials | None = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def verify_jwt(self, jwtoken: str) -> bool:
        isTokenValid: bool = False
        try:
            payload = jwt.decode(jwtoken, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        except JWTError:
            payload = None
        if payload:
            isTokenValid = True
        return isTokenValid
