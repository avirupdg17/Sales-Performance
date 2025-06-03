import os
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status, Form
from fastapi.responses import JSONResponse
from typing import Optional
from app.auth import get_current_user
from app.database.db import SalesDB

router = APIRouter(prefix="/user/profile", tags=["User Profile"])


@router.get("/")
def get_profile(current_user: dict = Depends(get_current_user)):
    phone = current_user["phone"]

    with SalesDB() as db:
        profile = db.get_records("users", [("phone", "=", phone)])
        if not profile:
            raise HTTPException(status_code=404, detail="Profile not found.")
    return profile[0]


@router.put("/photo")
async def update_own_photo(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user)
):
    user_phone = current_user["phone"]

    with SalesDB() as db:
        user = db.get_records("users", [("phone", "=", user_phone)])
        if not user:
            raise HTTPException(status_code=404, detail="User not found.")
        user = user[0]

        target_id = user["id"]
        content = await file.read()
        file_ext = os.path.splitext(file.filename)[1] or ".jpg"
        save_dir = "app/static/assets/profile"
        os.makedirs(save_dir, exist_ok=True)
        filename = f"{target_id}_profile_icon{file_ext}"
        save_path = os.path.join(save_dir, filename)

        old_photo_path = user.get("photo")
        if old_photo_path and os.path.exists(old_photo_path) and old_photo_path != save_path:
            try:
                os.remove(old_photo_path)
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Error deleting old photo: {str(e)}")

        with open(save_path, "wb") as f:
            f.write(content)

        db.update_user_profile(target_id, {"photo": save_path})

    return JSONResponse(content={"message": "Photo updated successfully"})

@router.put("/admin")
async def update_user_by_admin(
    id: int = Form(...),
    name: Optional[str] = Form(None),
    phone: Optional[str] = Form(None),
    email: Optional[str] = Form(None),
    role: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
    current_user: dict = Depends(get_current_user)
):
    if current_user["role"].lower() != "admin":
        raise HTTPException(status_code=403, detail="Only admins can update other users.")

    with SalesDB() as db:
        user = db.get_records("users", [("id", "=", id)])
        if not user:
            raise HTTPException(status_code=404, detail="User not found.")
        user = user[0]

        update_data = {}

        if name:
            update_data["name"] = name
        if phone:
            update_data["phone"] = phone
        if email:
            update_data["email"] = email
        if role:
            update_data["role"] = role

        if file:
            content = await file.read()
            file_ext = os.path.splitext(file.filename)[1] or ".jpg"
            save_dir = "app/static/assets/profile"
            os.makedirs(save_dir, exist_ok=True)
            filename = f"{id}_profile_icon{file_ext}"
            save_path = os.path.join(save_dir, filename)

            old_photo_path = user.get("photo")
            if old_photo_path and os.path.exists(old_photo_path) and old_photo_path != save_path:
                try:
                    os.remove(old_photo_path)
                except Exception as e:
                    raise HTTPException(status_code=500, detail=f"Error deleting old photo: {str(e)}")

            with open(save_path, "wb") as f:
                f.write(content)

            update_data["photo"] = save_path

        if not update_data:
            raise HTTPException(status_code=400, detail="No data provided to update.")
        
        db.update_records("users", [("id","=",id)], update_data)
        
    return JSONResponse(content={"message": "User profile updated by admin"})


@router.post("/add")
async def add_user(
    name: str = Form(...),
    username: str = Form(...),
    password: str = Form(...),
    role: str = Form(...),
    phone: str = Form(...),
    email: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
    current_user: dict = Depends(get_current_user)
):
    if current_user["role"].lower() != "admin":
        raise HTTPException(status_code=403, detail="Only admin can add users.")

    with SalesDB() as db:
        # Check if username already exists
        existing = db.get_records("users", [("phone", "=", phone)])
        if existing:
            raise HTTPException(status_code=400, detail="User already exists.")

        photo_path = None
        temp_photo_path = None

        if file:
            content = await file.read()
            save_dir = "app/static/assets/profile"
            os.makedirs(save_dir, exist_ok=True)

            temp_id = f"{username}_temp"
            ext = os.path.splitext(file.filename)[1] or ".jpg"
            filename = f"{temp_id}_profile_icon{ext}"
            temp_photo_path = os.path.join(save_dir, filename)

            with open(temp_photo_path, "wb") as f:
                f.write(content)

            photo_path = temp_photo_path  # temporary, will be renamed later

        user_data = {
            "name": name,
            "username": username,
            "password": password,
            "role": role,
            "email": email,
            "phone": phone,
            "photo": photo_path
        }

        db.add_record("users", user_data)
        user = db.get_records("users", [("phone", "=", phone)])
        user_id = user[0]["id"]

        if file and temp_photo_path:
            ext = os.path.splitext(temp_photo_path)[1]
            new_filename = f"{user_id}_profile_icon{ext}"
            new_path = os.path.join("app/static/assets/profile", new_filename)

            try:
                os.rename(temp_photo_path, new_path)
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Error renaming photo: {str(e)}")

            db.update_user_profile(user_id, {"photo": new_path})

    return JSONResponse(content={"message": "User added successfully", "user_id": user_id})


@router.delete("/delete")
def delete_user(
    id: int = Form(...),
    current_user: dict = Depends(get_current_user)
):
    if current_user["role"].lower() != "admin":
        raise HTTPException(status_code=403, detail="Only admin can delete users.")

    with SalesDB() as db:
        user_records = db.get_records("users", [("id", "=", id)])
        if not user_records:
            raise HTTPException(status_code=404, detail="User not found.")

        photo_path = user_records[0].get("photo")
        if photo_path and os.path.exists(photo_path):
            try:
                os.remove(photo_path)
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Error deleting profile photo: {str(e)}")

        db.delete_records("users", [("id", "=", id)])
        db.delete_records("performance", [("user_id", "=", id)])

    return JSONResponse(content={"message": f"User with ID {id} deleted successfully."})
