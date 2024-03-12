from typing import Annotated
from src.auth import oauth2Bearer
from fastapi import Depends, HTTPException, Request
from jose import JWTError, jwt
from src.env import secretKeyJWT, algorithmJWT
from starlette import status

async def verifyJWT(token: Annotated[str, Depends(oauth2Bearer)], request: Request):
    try:
      payload = jwt.decode(token, secretKeyJWT, algorithms=[algorithmJWT])
      userId = payload.get('sub')
      if not userId:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could Not Validate User")
      tokenCookie = request.cookies.get("access_token")
      payloadCookie = jwt.decode(tokenCookie, secretKeyJWT, algorithms=[algorithmJWT])
      userId = payloadCookie.get('sub')
      if not userId:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could Not Validate User")
      return { 'userId' : int(userId) }
    except JWTError:
       raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could Not Validate User")
 