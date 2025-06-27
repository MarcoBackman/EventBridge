from pydantic import BaseModel, Field
from datetime import datetime
from app.enums.license_type import LicenseType

class LicenseResponse(BaseModel):
    success: bool = Field(default=False)
    message: str = Field(default="")
    isError: bool = Field(default=False)
    useLimit: int = Field(default=0)
    hashedLicenseKey: str = Field(default="")
    errorMessage: str = Field(default="")
    licenseType: LicenseType = Field(default=None)
    expirationDate: datetime = Field(default=datetime.now())