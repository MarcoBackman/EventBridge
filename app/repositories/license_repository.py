from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import or_, and_
from datetime import datetime
from app.models.schema.license_schema import LicenseCreate, LicenseUpdate, License as LicenseSchema
from typing import AsyncGenerator

class LicenseRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_license(self, license_data: LicenseCreate) -> LicenseSchema:
        db_license = LicenseSchema(**license_data.model_dump()) 
        
        self.db.add(db_license)
        await self.db.commit()
        await self.db.refresh(db_license) # This refreshes db_license with DB-generated IDs, dates, etc.
        return db_license

    async def get_license_by_id(self, license_id: int) -> Optional[LicenseSchema]:
        result = await self.db.execute(select(LicenseSchema).filter(LicenseSchema.license_id == license_id))
        return result.scalar_one_or_none()

    async def get_license_by_key(self, license_key: str) -> Optional[LicenseSchema]:
        result = await self.db.execute(select(LicenseSchema).filter(LicenseSchema.license_key == license_key))
        return result.scalar_one_or_none()

    async def get_all_licenses(
        self,
        skip: int = 0,
        limit: int = 100,
        is_used: Optional[bool] = None,
        is_blocked: Optional[bool] = None,
        search_query: Optional[str] = None
    ) -> List[LicenseSchema]:
        query = select(LicenseSchema)
        if is_used is not None:
            query = query.filter(LicenseSchema.is_used == is_used)
        if is_blocked is not None:
            query = query.filter(LicenseSchema.is_blocked == is_blocked)
        if search_query:
            query = query.filter(
                or_(
                    LicenseSchema.license_key.ilike(f"%{search_query}%"),
                    LicenseSchema.license_key_hint.ilike(f"%{search_query}%")
                )
            )

        query = query.offset(skip).limit(limit)
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def update_license(self, license: LicenseSchema, license_data: LicenseUpdate) -> LicenseSchema:
        update_data = license_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(license, key, value)

        await self.db.commit()
        await self.db.refresh(license)
        return license

    async def delete_license(self, license: LicenseSchema) -> None:
        await self.db.delete(license)
        await self.db.commit()

    async def mark_license_as_used(self, license: LicenseSchema) -> LicenseSchema:
        license.use_counts += 1
        license.last_used_date = datetime.now()
        if license.use_counts >= license.use_limit:
            license.is_used = True
        await self.db.commit()
        await self.db.refresh(license)
        return license

    async def block_license(self, license: LicenseSchema) -> LicenseSchema:
        license.is_blocked = True
        await self.db.commit()
        await self.db.refresh(license)
        return license

    async def unblock_license(self, license: LicenseSchema) -> LicenseSchema:
        license.is_blocked = False
        await self.db.commit()
        await self.db.refresh(license)
        return license