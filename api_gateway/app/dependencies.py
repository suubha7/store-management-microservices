from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer(
    scheme_name="BearerAuth",
    description="Enter: Bearer <access_token>"
)


# Dependency to validate token
def require_bearer_token(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    if credentials.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization scheme"
        )

    return credentials