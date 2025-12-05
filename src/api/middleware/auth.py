from fastapi import Request, HTTPException
import os
import jwt
SECRET_KEY=os.getenv("JWT_SECRET","local_code")
async def verify_auth(request:Request,call_next):
    if request.url.path.startswith(("/docs","/openai.json")):
        return await call_next(request)
    token=request.headers.get("Authorization")
    if not token:
        raise HTTPException(status_code=401,detail="Missing auth token")
    try:
        jwt.decode(token.replace("Bearer ",""),SECRET_KEY,algorithms=["HS256"])
        response=await call_next(request)
        return response
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401,detail="Token expired")
    except Exception:
        raise HTTPException(status_code=401,detail="Invalid token")