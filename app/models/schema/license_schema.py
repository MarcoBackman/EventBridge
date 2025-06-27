from pydantic import BaseModel, Field, StringConstraints
from typing import Optional
from datetime import datetime
from typing_extensions import Annotated
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class License(Base):
    __tablename__ = "client_download_license" # Your table name

    license_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    license_key = Column(String(200), unique=True, nullable=False)
    created_date = Column(DateTime, default=datetime.now, nullable=False)
    last_used_date = Column(DateTime, default=datetime.now)
    is_used = Column(Boolean, default=False, nullable=False)
    is_blocked = Column(Boolean, default=False, nullable=False)
    expiration_date = Column(DateTime, nullable=True) # Matches TIMESTAMP NULL
    use_counts = Column(Integer, default=0, nullable=False)
    use_limit = Column(Integer, default=10, nullable=False)
    license_key_hint = Column(String(50), nullable=False) # From your ALTER TABLE
    license_type = Column(String(50), nullable=False)
    # You might want to add a type field to match the LicenseType enum
    # license_type = Column(Integer, default=0, nullable=False) # Or String/Enum type if mapped as such

    def __repr__(self):
        return f"<License(id={self.license_id}, key={self.license_key[:10]}, used={self.is_used})>"

class LicenseCreate(BaseModel):
    license_key: Annotated[str, StringConstraints(min_length=1, max_length=200)] = Field(
        ...,
        description="The unique license key."
    )
    license_key_hint: Annotated[str, StringConstraints(min_length=1, max_length=50)] = Field(
        ...,
        description="A short hint or description for the license key."
    )
    expiration_date: Optional[datetime] = Field(
        None,
        description="The date and time when the license key expires. Nullable."
    )
    use_limit: int = Field(
        10, # Default value
        ge=1, # Greater than or equal to 1
        description="The maximum number of times the license key can be used. Default is 10."
    )
    license_type: Annotated[str, StringConstraints(min_length=1, max_length=50)] = Field(
        ...,
        description="A short hint or description for the license key."
    )
    
# For updating an existing license (all fields optional)
class LicenseUpdate(BaseModel):
    license_key: Optional[Annotated[str, StringConstraints(min_length=1, max_length=200)]] = Field(
        None,
        description="The unique license key (if allowed to change)."
    )
    is_blocked: Optional[bool] = Field(
        None,
        description="Whether the license key is blocked. (Typically managed by admin)."
    )
    is_used: Optional[bool] = Field(None)
    expiration_date: Optional[datetime] = Field(
        None,
        description="The new expiration date for the license key. Nullable."
    )
    use_limit: Optional[int] = Field(
        None,
        ge=1,
        description="The new maximum number of times the license key can be used."
    )
    license_key_hint: Optional[Annotated[str, StringConstraints(min_length=1, max_length=50)]] = Field(
        None,
        description="A new short hint or description for the license key."
    )
    use_counts: Optional[int] = Field(
        None
    )

    license_type: Optional[str] = Field(
        None
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "is_blocked": True,
                "expiration_date": "2027-06-23T00:00:00", # Current year + 2
                "use_limit": 100
            }
        }
    }
