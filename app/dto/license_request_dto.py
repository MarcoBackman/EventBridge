from pydantic import BaseModel, Field, StringConstraints
from typing import Optional
from datetime import datetime
from typing_extensions import Annotated
from app.enums.license_type import LicenseType

#Case 1 when admin requests for a single license generation
class LicenseGenerateRequest(BaseModel):
    raw_key: str = Field(alias="rawKey")
    license_type: LicenseType = Field(defualt=0, alias="licenseType")
    expiration_date: Optional[datetime] = Field(None, alias="expirationDate")
    use_limit: int = Field(10, ge=1, alias="useLimit")

    #CLIENT_DOWNLOAD_LICENSE = 1
    #CLIENT_SUBSCRIPTION_LICENSE = 2
    #DEMO_LICENSE = 3

    model_config = {
        "json_schema_extra": {
            "example": {
                "rawKey": "ABCDEFGHIJKLM",
                "licenseType": 1,
                "expirationDate": "2025-12-31T23:59:59",
                "useLimit": 50
            }
        }
    }

#Case 2 when user brings in the license code and requires validation
class LicenseValidateRequest(BaseModel):
    license_key: str = Field(alias="licenseKey")

    model_config = {
        "json_schema_extra": {
            "example": {
                "licenseKey": "ABCDEFGHIJKLM",
            }
        }
    }


#Case 3 when user uses the license on use
class LicenseUseRequest(BaseModel):
    license_key: str = Field(alias="licenseKey")

    model_config = {
        "json_schema_extra": {
            "example": {
                "licenseKey": "ABCDEFGHIJKLM",
            }
        }
    }

#Case 4 toggles user license access
class LicenseBlockToggle(BaseModel):
    license_key: str = Field(alias="licenseKey")
    toggle_block: bool = Field(alias="toggleBlock")

    model_config = {
        "json_schema_extra": {
            "example": {
                "licenseKey": "ABCDEFGHIJKLM",
                "toggleBlock": True,
            }
        }
    }


#Case 4 resets license usage amount
class ResetLicenseAmtRequest(BaseModel):
    license_key: str = Field(alias="licenseKey")

    model_config = {
        "json_schema_extra": {
            "example": {
                "licenseKey": "ABCDEFGHIJKLM",
            }
        }
    }

#Case 5 increase license limit amount by given value
class IncreaseLicenseUsageLimitAmtRequest(BaseModel):
    license_key: str = Field(alias="licenseKey")
    increase_amt: int = Field(alias="increaseAmount")

    model_config = {
        "json_schema_extra": {
            "example": {
                "licenseKey": "ABCDEFGHIJKLM",
                "increaseAmount" : 10
            }
        }
    }

#Case 6 decrease license limit amount by given value
class DecreaseLicenseUsageLimitAmtRequest(BaseModel):
    license_key: str = Field(alias="licenseKey")
    decrease_amt: int = Field(alias="decreaseAmount")
    model_config = {
        "json_schema_extra": {
            "example": {
                "licenseKey": "ABCDEFGHIJKLM",
                "decreaseAmount" : 10
            }
        }
    }

