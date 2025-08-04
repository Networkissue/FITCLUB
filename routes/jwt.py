# from fastapi import Depends, HTTPException, status
# from datetime import datetime, timedelta
# from typing import Optional
# from fastapi.security import OAuth2PasswordBearer
# from jose import jwt, ExpiredSignatureError, JWTError
# from database.database import user_data

# # Configuration (Replace these with your actual values)
# SECRET_KEY = "your_secret_key"  # Secret key for encoding and decoding the JWT
# ALGORITHM = "HS256"             # Algorithm used for encoding and decoding
# ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Default expiration time in minutes


# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/signin")

# def create_access_token(data: dict, expires_in: Optional[timedelta] = None) -> str:
#     """
#     Creates a JWT access token.
    
#     data (dict): The data to encode in the token.
#     expires_in (Optional[timedelta]): Optional expiration time for the token.
        
#     Returns:
#         str: The encoded JWT token.
#     """
#     # Make a copy of the data to avoid modifying the original dictionary
#     token_data = data.copy()

#     # Set the expiration time for the token
#     if expires_in:
#         expire_at = datetime.utcnow() + expires_in
#     else:
#         expire_at = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
#     # Add the expiration time to the payload
#     token_data.update({"exp": expire_at})

#     # Encode the token using the secret key and algorithm
#     encoded_jwt = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)

#     return encoded_jwt

# def decode_access_token(token: str) -> dict:
#     try:
#         # Decode the token and retrieve the payload
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         print(f"👆 Token decoded: {payload}")  # Check if token is decoded correctly

#         # Validate expiration time
#         expiration_time = datetime.utcfromtimestamp(payload.get("exp"))
#         if expiration_time <= datetime.utcnow():
#             raise ExpiredSignatureError("Token has expired")
        
#         return payload  # Return decoded payload if valid
#     except ExpiredSignatureError:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             headers={"WWW-Authenticate": "Bearer"},
#             detail="Token has expired"
#         )
#     except JWTError:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             headers={"WWW-Authenticate": "Bearer"},
#             detail="Invalid token"
#         )


# def get_user_by(token: str = Depends(oauth2_scheme)) -> dict:
#     print(f"👆 Received token: {token}")  # Debugging print statement
    
#     try:
#         payload = decode_access_token(token)
#         print(f"👆 Payload after decoding: {payload}")  # Debugging print statement
        
#         if payload and "sub" in payload:
#             user = user_data.find_one({"email": payload["sub"]})
            
#             if user:
#                 print(f"👆 User found: {user}")  # Debugging print statement
#                 return user
#             else:
#                 print("❌ User not found in the database.")  # Debugging print statement
#                 raise HTTPException(status_code=404, detail="User not found")
#     except JWTError:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid token"
#         )
    
#     return None


from fastapi import Request, HTTPException, status
from datetime import datetime, timedelta
from jose import jwt, JWTError
from typing import Optional
from database.database import user_data

# JWT Config
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 3000


def create_access_token(data: dict, expires_in: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_in or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> dict:
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])


def get_user_by_cookie(request: Request) -> dict:
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    try:
        if token.startswith("Bearer "):
            token = token[len("Bearer "):]
        payload = decode_access_token(token)
        user = user_data.find_one({"email": payload.get("sub")})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
