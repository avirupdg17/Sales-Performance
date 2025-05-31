from fastapi import APIRouter, FastAPI, Depends, HTTPException, status
from app.auth import get_current_user
from app.profile import router as profile_router
from app.database.db import SalesDB
from app.routers import upload_excel
from app.auth import (
    router as auth_router,
    SECRET_KEY,
    ALGORITHM,
    get_current_user  
)

app = FastAPI(debug=True)

# Public root endpoint
@app.get("/")
def read_root():
    return {"message": "hello"}

# Sample performance fetch endpoint (from database)
@app.get("/performance")
def get_performance(current_user: dict = Depends(get_current_user)):
    username = current_user["username"]
    with SalesDB() as db:
        # Get user record by username to find user_id
        user = db.get_records("users", [("username", "=", username)])
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        user_id = user[0]["id"]

        # Filter performance by user_id
        data = db.get_records("performance", [("user_id", "=", user_id)])

    return data

# Example protected route to verify token and role
@app.get("/protected-route")
async def protected_route(current_user: dict = Depends(get_current_user)):
    return {
        "message": f"Hello {current_user['username']} with role {current_user['role']}"
    }

# Include authentication routes
app.include_router(auth_router)

# Include profile routes
app.include_router(profile_router)

test_router = APIRouter()

@test_router.get("/test/users")
def list_users():
    with SalesDB() as db:
        users = db.get_records("users")
        # Hide passwords for safety if you want
      
        return users

app.include_router(upload_excel.router)