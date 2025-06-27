from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from typing_extensions import Annotated

# For responding with license data
class License(BaseModel):
    license_id: Optional[int]
    license_key: str
    created_date: datetime
    last_used_date: Optional[datetime]
    is_used: bool
    is_blocked: bool
    expiration_date: Optional[datetime]
    use_counts: int
    use_limit: int
    license_key_hint: str
    license_type: str

    model_config = {
        "from_attributes": True, # This replaces orm_mode = True in Pydantic V1
        "json_schema_extra": {
            "example": {
                "license_id": 1,
                "license_key": "UNIQUE-LICENSE-ABC-123",
                "created_date": "2024-01-01T10:00:00",
                "last_used_date": "2025-06-23T10:30:00", # Current date
                "is_used": True,
                "is_blocked": False,
                "expiration_date": "2025-12-31T23:59:59",
                "use_counts": 5,
                "use_limit": 50,
                "license_key_hint": "For premium access",
                "license_type": "CLIENT_LICENSE_DOWNLOAD"
            }
        }
    }
