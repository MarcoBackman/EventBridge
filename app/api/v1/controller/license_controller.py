from fastapi import APIRouter, status, Depends
from app.dto.license_request_dto import LicenseGenerateRequest, LicenseUseRequest, LicenseValidateRequest, LicenseBlockToggle, ResetLicenseAmtRequest, IncreaseLicenseUsageLimitAmtRequest, DecreaseLicenseUsageLimitAmtRequest
from app.dto.license_response_dto import LicenseResponse
from app.models.schema.license_schema import License as LicenseSchema
from app.services.license_service import LicenseService
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
import logging

license_router = APIRouter(prefix="/license", tags=["License"])
logger = logging.getLogger(__name__)

async def get_license_service(db: AsyncSession = Depends(get_db)) -> LicenseService:
    return LicenseService(db=db)

@license_router.post("/register-license", status_code=status.HTTP_200_OK)
async def generate_license(
    request: LicenseGenerateRequest,
    license_service: LicenseService = Depends(get_license_service)
) -> LicenseResponse:

    license_hint = "X" * 4 + request.raw_key[4:-2] + "X" * 2

    response = LicenseResponse()
    try:
        pass
        result : LicenseSchema = await license_service.convert_to_hashed_license_entry(
            request.raw_key,
            request.expiration_date,
            request.use_limit,
            license_hint,
            request.license_type
        )

        if result is None:
            logger.warning("Failed to create license key. Possible duplication")
            response.success = False
            response.isError = True
            response.errorMessage = "License creation failed due to the server error. Possible ducplicate key."
            return response

        response.success = True
        response.isError = False
        response.message = "License key successfully generated. " + result.license_key_hint
        response.expirationDate = result.expiration_date
        response.useLimit = result.use_limit
        response.licenseType = request.license_type

    except NotImplementedError as e:
        logger.error(f"License creation method not implemented: {e}", exc_info=True)
        response.success = False
        response.isError = True
        response.errorMessage = "License creation feature is not yet implemented."
    except Exception as e:
        logger.error(f"Failed to create license key: {e}", exc_info=True)
        response.success = False
        response.isError = True
        response.message = "Failed to create license key."
        response.errorMessage = f"An unexpected error occurred: {str(e)}"
    return response

@license_router.post("/validate-license", status_code=status.HTTP_200_OK)
async def validate_license(
    request: LicenseValidateRequest,
    license_service: LicenseService = Depends(get_license_service)
) -> LicenseResponse:
    result : LicenseSchema = await license_service.verify_license(request.license_key)

    response = LicenseResponse()
    if result is None:
        response.success = False
        response.message = "User is not allowed to use provided license key"
        response.isError = True
        return response

    response.success = True
    response.message = "user can still use this license"
    response.licenseType = result.license_key_hint
    response.isError = False
    return response


@license_router.patch("/license-increase-count", status_code=status.HTTP_200_OK)
async def license_increase_count(
    request: LicenseUseRequest,
    license_service: LicenseService = Depends(get_license_service)
) -> LicenseResponse:
    result : LicenseSchema = await license_service.verify_and_use_license(request.license_key)

    response = LicenseResponse()
    if result is None:
        response.success = False
        response.message = "User is not allowed to use provided license key"
        response.isError = True

    response.success = True
    response.message = "User has used the license"
    response.licenseType = result.license_key_hint
    response.isError = False
    return response

@license_router.patch("/toggle-license-block", status_code=status.HTTP_200_OK)
async def set_license_in_use(
    request: LicenseBlockToggle,
    license_service: LicenseService = Depends(get_license_service)
) -> bool:
    result = await license_service.toggle_license(request.license_key, request.toggle_block)
    return result

@license_router.patch("/reset-usage", status_code=status.HTTP_200_OK)
async def set_license_in_use(
    request: ResetLicenseAmtRequest,
    license_service: LicenseService = Depends(get_license_service)
) -> bool:
    result = await license_service.reset_usage(request.license_key)
    return result

@license_router.patch("/increase-limit", status_code=status.HTTP_200_OK)
async def set_license_in_use(
    request: IncreaseLicenseUsageLimitAmtRequest,
    license_service: LicenseService = Depends(get_license_service)
) -> bool:
    result = await license_service.increase_usage_limit(request.license_key, request.increase_amt)
    return result


@license_router.patch("/decrease-limit", status_code=status.HTTP_200_OK)
async def set_license_in_use(
    request: DecreaseLicenseUsageLimitAmtRequest,
    license_service: LicenseService = Depends(get_license_service)
) -> bool:
    result = await license_service.decrease_usage_limit(request.license_key, request.decrease_amt)
    return result