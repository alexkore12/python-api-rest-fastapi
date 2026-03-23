"""
Módulo de Autenticación JWT
Proporciona autenticación y autorización para la API
"""
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import JWTError, jwt
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import os

# Configuración
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Security scheme
security = HTTPBearer(auto_error=False)


class TokenData(BaseModel):
    """Datos del token JWT"""
    sub: str  # username
    exp: Optional[datetime] = None


class User(BaseModel):
    """Modelo de usuario"""
    username: str
    disabled: bool = False


# Base de datos de usuarios (en memoria para demo)
# En producción, usar una base de datos real
users_db: Dict[str, Dict[str, Any]] = {
    "admin": {
        "username": "admin",
        "hashed_password": "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYzS.xJ5m3G",  # password: admin123
        "disabled": False,
        "role": "admin"
    },
    "user": {
        "username": "user",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",  # password: password
        "disabled": False,
        "role": "user"
    }
}


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Crear token de acceso JWT"""
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire.isoformat()})
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> TokenData:
    """Verificar token JWT"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        sub: str = payload.get("sub")
        
        if sub is None:
            raise credentials_exception
            
        token_data = TokenData(sub=sub)
        return token_data
        
    except JWTError:
        raise credentials_exception


def get_current_user(credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)) -> User:
    """Obtener usuario actual desde el token"""
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token = credentials.credentials
    token_data = verify_token(token)
    
    user = users_db.get(token_data.sub)
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    return User(
        username=user["username"],
        disabled=user["disabled"]
    )


def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """Verificar que el usuario esté activo"""
    if current_user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    return current_user


# Credenciales mock para login
def authenticate_user(username: str, password: str) -> Optional[User]:
    """Autenticar usuario (demo)"""
    user = users_db.get(username)
    
    if not user:
        return None
    
    # En producción, usar bcrypt para verificar passwords
    # Por ahora, aceptamos cualquier password para demo
    # Verificación real: bcrypt.checkpw(password.encode(), user["hashed_password"].encode())
    
    if user["disabled"]:
        return None
    
    return User(
        username=user["username"],
        disabled=user["disabled"]
    )
