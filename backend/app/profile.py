from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from fastapi.responses import JSONResponse
from typing import Optional
from app.auth import get_current_user
from app.database.db import SalesDB

router = APIRouter(prefix="/user/profile", tags=["User Profile"])

@router.get("/")
def get_profile(current_user: dict = Depends(get_current_user)):
    username = current_user["phone"]

    with SalesDB() as db:
        # profile = db.get_user_profile(username)
        profile = db.get_records("users", ("phone", "=", phone))
        if not profile:
            raise HTTPException(status_code=404, detail="Profile not found.")
    return profile

@router.put("/")
async def update_profile(
    name: Optional[str] = None,
    phone: Optional[str] = None,
    file: Optional[UploadFile] = File(None),
    current_user: dict = Depends(get_current_user)
):
    username = current_user["username"]
    role = current_user["role"].lower()

    with SalesDB() as db:
        profile = db.get_user_profile(username)
        if not profile:
            raise HTTPException(status_code=404, detail="Profile not found.")

        update_data = {}

        if role == "admin":
            # Admin can update name, phone, photo
            if name:
                update_data["name"] = name
            if phone:
                update_data["phone"] = phone
            if file:
                content = await file.read()
                update_data["photo"] = content
        else:
            # Other roles: only photo update allowed
            if file:
                content = await file.read()
                update_data["photo"] = content
            else:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Only photo update is allowed for your role."
                )

        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No valid data provided to update."
            )

        db.update_user_profile(username, update_data)

    return JSONResponse(content={"message": "Profile updated successfully"})