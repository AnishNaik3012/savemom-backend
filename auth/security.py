from jose import jwt
from datetime import datetime, timedelta

SECRET_KEY = "dev-secret"
ALGORITHM = "HS256"


def create_token(identifier: str) -> str:
    payload = {
        "sub": identifier,
        "exp": datetime.utcnow() + timedelta(days=1),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
