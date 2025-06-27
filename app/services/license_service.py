from datetime import datetime
from typing import Optional
from passlib.context import CryptContext
from app.utils.license_key_generator import convert_to_hashed_license_key
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.license_repository import LicenseRepository
from app.models.license import License
from app.models.schema.license_schema import LicenseCreate, LicenseUpdate, License as LicenseSchema
from app.enums.license_type import LicenseType
from dateutil.relativedelta import relativedelta
from app.core.config import settings
from fastapi import HTTPException
import logging

logger = logging.getLogger(__name__)

class LicenseService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.pwd_context = CryptContext(schemes=[settings.ALGORITHM], deprecated="auto")
        self.license_repo: LicenseRepository = LicenseRepository(db=self.db)
        
    async def verify_license(
        self,
        raw_license_key: str
    ) -> bool:
        logging.debug("verifying a given license")

        hashed_license_key = convert_to_hashed_license_key(raw_license_key)
        licenseData : LicenseSchema = await self.license_repo.get_license_by_key(hashed_license_key)
    
        #Todo: instead of return None, return exception types that represents the issue
        if licenseData is None:
            return None
        
        if licenseData.use_counts >= licenseData.use_limit:
            return None

        return licenseData

    async def verify_and_use_license(
        self,
        raw_license_key: str,
    ) -> Optional[License]:
        logging.debug("verifying a given license and incrementing the usage")

        hashed_license_key = convert_to_hashed_license_key(raw_license_key)

        licenseData : LicenseSchema = await self.license_repo.get_license_by_key(hashed_license_key)
        
        if licenseData is None:
            return None
        
        if licenseData.use_counts >= licenseData.use_limit:
            return None
    


        #on valid license, increase current usage by one - set db
        licenseUpdate : LicenseUpdate = LicenseUpdate()
        if (licenseData.use_counts >= 0):
            licenseUpdate.is_used = True
        licenseUpdate.use_counts = licenseData.use_counts + 1
        return await self.license_repo.update_license(licenseData, licenseUpdate)

    async def convert_to_hashed_license_entry(
        self,
        raw_key: str,
        expiration_date: Optional[datetime] = None,
        use_limit: int = 10,
        license_hint: str = "UNKNOWN_HINT",
        license_type: str = "UNKNOWN_TYPE"
    ) -> License:
        logger.debug("creating a new license")

        hashed_key = convert_to_hashed_license_key(raw_key)

        if (expiration_date is None):
            expiration_date = datetime.now + relativedelta(months=1)

        license_data = LicenseCreate(
            license_key=hashed_key,
            license_type=license_type,
            license_key_hint=license_hint,
            expiration_date=expiration_date,
            use_limit=use_limit
        )

        #Add into DB
        try:
            created_orm_license: License = await self.license_repo.create_license(license_data)
            logger.debug(f"Created ORM License: {created_orm_license}")
            created_orm_license.license_key = "" #Security! Do not disclose license_key
            return created_orm_license
        except HTTPException as e:
            logger.info(f"License creation failed due to: {e.detail} for key: {license_data.license_key}")
            return None
        except Exception as e:
            logger.error(f"An unexpected error occurred during license creation: {e}", exc_info=True)
            return None
        
    async def toggle_license(self, license_key_raw : str, toggleBlock: bool) -> bool:
        logger.debug(f"Setting toggle to disable/enable license use")

        hashed_key = convert_to_hashed_license_key(license_key_raw)

        #first, verify if licnese exists
        licenseData : LicenseSchema = await self.license_repo.get_license_by_key(hashed_key)

        if licenseData is None:
            logger.info(f"License not found. provided licnese key={license_key_raw}")
            return False
        
        if licenseData.is_blocked == toggleBlock:
            logger.info(f"License is already set as desired. is_blocked={toggleBlock}")
            return False

        #set license usage
        if toggleBlock == True:
            await self.license_repo.block_license(licenseData)
        else:
            await self.license_repo.unblock_license(licenseData)
        return True
    
    async def reset_usage(self, license_key_raw: str) -> bool:
        logger.debug(f"Resetting license key usage")

        hashed_key = convert_to_hashed_license_key(license_key_raw)
        licenseData : LicenseSchema = await self.license_repo.get_license_by_key(hashed_key)

        if licenseData is None:
            logger.info(f"License not found. provided licnese key={license_key_raw}")
            return False
        
        licenseUpdate : LicenseUpdate = LicenseUpdate()
        licenseUpdate.use_counts = 0
        await self.license_repo.update_license(licenseData, licenseUpdate)
        return True
    
    async def increase_usage_limit(self, license_key_raw: str, increase_amt: int) -> bool:
        logger.debug(f"Increasing license key usage limit")

        hashed_key = convert_to_hashed_license_key(license_key_raw)
        licenseData : LicenseSchema = await self.license_repo.get_license_by_key(hashed_key)

        if licenseData is None or licenseData.use_limit is None:
            logger.info(f"License not found. provided licnese key={license_key_raw}")
            return False
        
        licenseUpdate : LicenseUpdate = LicenseUpdate()
        licenseUpdate.use_limit = licenseData.use_limit + increase_amt
        await self.license_repo.update_license(licenseData, licenseUpdate)
        return True
    

    async def decrease_usage_limit(self, license_key_raw: str, decrease_amt: int) -> bool:
        logger.debug(f"Decreasing license key usage limit")

        hashed_key = convert_to_hashed_license_key(license_key_raw)
        licenseData : LicenseSchema = await self.license_repo.get_license_by_key(hashed_key)

        if licenseData is None:
            logger.info(f"License not found. provided licnese key={license_key_raw}")
            return False

        if licenseData.use_limit <= 0:
            logger.warning(f"Use limit already at the bottom. Licensekey={license_key_raw}")
            return False

        licenseUpdate : LicenseUpdate = LicenseUpdate()
        licenseUpdate.use_limit = licenseData.use_limit - decrease_amt
        
        if licenseData.use_counts >= licenseUpdate.use_limit:
            logger.warning(f"You are decresing the limit under the current usage for license_key={license_key_raw}")

        await self.license_repo.update_license(licenseData, licenseUpdate)
        return True