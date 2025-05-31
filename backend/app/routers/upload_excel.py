from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from io import BytesIO
from app.services.excel_parser import parse_excel
from app.database.db import SalesDB
from app.auth import get_current_user
import base64


router = APIRouter()

@router.post("/upload-excel")
async def upload_excel(
    file: UploadFile = File(...),
    # current_user: dict = Depends(get_current_user)
):
    # if current_user["role"].lower() != "admin":
        # raise HTTPException(status_code=403, detail="Only Admin can upload Excel data.")

    contents = await file.read()
    encoded = base64.b64encode(contents).decode("utf-8")
    # return {"contents": encoded}

    try:
        parsed = parse_excel(BytesIO(contents))
        print(parsed,flush=True)
        with SalesDB() as db:
            for perf in parsed["performance"]:
                db.add_record("performance", perf)

            return {
                 "message": "Excel data uploaded successfully.",
                  "parsed_data": db.get_records("performance")
            }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error parsing Excel: {e}")