from App.src.models import Admin
from App.src.schema import AdminRequestSchema, AdminUpdateSchema
from App.src.logics import generate_password
from App.src.utils import mapping_null_values
from fastapi import HTTPException, status


class AdminLogic:
    @staticmethod
    async def create(obj: AdminRequestSchema):
        obj.password = generate_password(obj.password)
        admin = await Admin.create(**dict(obj))

        return admin

    @staticmethod
    async def get_by_id(id: str, adminname: str = None):
        admin = await admin.get_by_id(id)
        print(f"<admin{admin.adminname}")
        if admin.adminname == adminname:
            return admin
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    @staticmethod
    async def update(obj: AdminUpdateSchema):
        if obj.password is not None:
            obj.password = generate_password(obj.password)

        admin = await Admin.get_by_id(obj.id)
        admin = mapping_null_values(dict(obj), admin.__dict__)
        await Admin.update(admin)

        return admin

    @staticmethod
    async def delete(id: str):
        await Admin.delete(id)

        return {"message": "Admin deleted successfully"}
