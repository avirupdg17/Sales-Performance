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
    date: str = Form(...),  # Added this line to accept the date as form data
    # current_user: dict = Depends(get_current_user)
):
    # if current_user["role"].lower() != "admin":
    #     raise HTTPException(status_code=403, detail="Only Admin can upload Excel data.")

    # Validate date format
    try:
        kpi_date = datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")

    contents = await file.read()
    encoded = base64.b64encode(contents).decode("utf-8")
    # return {"contents": encoded}

    try:
        # Pass the kpi_date to parse_excel
        parsed = parse_excel(BytesIO(contents), kpi_date)
        print(parsed, flush=True)
        with SalesDB() as db:
            for perf in parsed["performance"]:
                db.add_record("performance", perf)

            return {
                "message": "Excel data uploaded successfully.",
                "parsed_data": db.get_records("performance")
            }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error parsing Excel: {e}")