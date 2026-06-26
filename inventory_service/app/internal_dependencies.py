import os
from dotenv import load_dotenv
from fastapi import Header, HTTPException, status

load_dotenv()

INTERNAL_SERVICE_KEY = os.getenv("INTERNAL_SERVICE_KEY")


# Verify internal service API key
def verify_internal_service_key(x_internal_service_key: str | None = Header(default=None)):
    if not INTERNAL_SERVICE_KEY:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="Internal service key is not configured")

    if x_internal_service_key != INTERNAL_SERVICE_KEY:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Internal service access denied")