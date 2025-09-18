import hashlib
import jwt
from datetime import datetime, timedelta
from typing import Optional
import os
from ..models import User, UserCreate, UserLogin, UserResponse

class AuthService:
    def __init__(self):
        # Use a secret key for JWT encoding/decoding
        self.secret_key = os.environ.get('JWT_SECRET', 'streamflix-secret-key-change-in-production')
        self.algorithm = 'HS256'
        self.access_token_expire = timedelta(days=30)  # 30 days for demo
    
    def hash_password(self, password: str) -> str:
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def verify_password(self, password: str, hashed_password: str) -> bool:
        """Verify password against hash"""
        return self.hash_password(password) == hashed_password
    
    def create_access_token(self, user_id: str, email: str) -> str:
        """Create JWT access token"""
        expire = datetime.utcnow() + self.access_token_expire
        payload = {
            "user_id": user_id,
            "email": email,
            "exp": expire,
            "iat": datetime.utcnow()
        }
        
        token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
        return token
    
    def decode_token(self, token: str) -> Optional[dict]:
        """Decode and validate JWT token"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.JWTError:
            return None
    
    def get_current_user_id(self, token: str) -> Optional[str]:
        """Extract user ID from JWT token"""
        payload = self.decode_token(token)
        if payload:
            return payload.get("user_id")
        return None