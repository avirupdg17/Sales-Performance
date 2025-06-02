import os
from fastapi import UploadFile, File, Form, Depends, HTTPException, APIRouter
from datetime import datetime
from app.auth import get_current_user

router = APIRouter()

@router.post("/upload-incentive")
async def upload_incentive_image(
    file: UploadFile = File(...),
    role: str = Form(...),  # Frontend sends this implicitly based on current sidebar context
    date: str = Form(...),  # Format: YYYY-MM
    current_user: dict = Depends(get_current_user)
):
    if current_user["role"].lower() != "admin":
        raise HTTPException(status_code=403, detail="Only Admin can upload incentive schemes.")

    # Parse and validate date
    try:
        parsed_date = datetime.strptime(date, "%Y-%m")
        month = parsed_date.month
        year = parsed_date.year
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM.")

    # Validate file extension
    if not file.filename.lower().endswith((".jpg", ".jpeg", ".png")):
        raise HTTPException(status_code=400, detail="Only JPG, JPEG, or PNG files are allowed.")

    # Normalize and sanitize role
    role = role.lower()
    filename = f"incentives_{role}_{month:02d}_{year}.jpg"
    save_dir = "app/static/assets/incentive"
    os.makedirs(save_dir, exist_ok=True)
    save_path = os.path.join(save_dir, filename)

    # Save file
    contents = await file.read()
    with open(save_path, "wb") as f:
        f.write(contents)

    return {
        "message": "Incentive image uploaded successfully.",
        "file_saved_as": filename
    }