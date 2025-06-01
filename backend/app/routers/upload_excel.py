from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from io import BytesIO
from app.services.excel_parser import parse_excel
from app.database.db import SalesDB
from app.auth import get_current_user
import base64
from datetime import datetime

router = APIRouter()

@router.post("/upload-excel")
async def upload_excel(
    file: UploadFile = File(...),
    date: str = Form(...),
    current_user: dict = Depends(get_current_user)
):
    if current_user["role"].lower() != "admin":
        raise HTTPException(status_code=403, detail="Only Admin can upload Excel data.")

    try:
        kpi_date = datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")

    contents = await file.read()

    try:
        parsed = parse_excel(BytesIO(contents), kpi_date)

        with SalesDB() as db:
            for perf in parsed["performance"]:
                user_phone = perf.pop("user_phone", None)
                if not user_phone:
                    continue  # skip if no phone

                # Lookup user_id by phone
                user_records = db.get_records("users", [("phone", "=", user_phone)])
                if not user_records:
                    # Optionally: skip or raise error for unknown users
                    continue
                user_id = user_records[0]["id"]

                # Replace user_phone with user_id
                perf["user_id"] = user_id

                # Now insert the performance record
                db.add_record("performance", perf)

            return {
                "message": "Excel data uploaded successfully.",
                "parsed_data": db.get_records("performance")
            }

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error parsing Excel: {e}")
