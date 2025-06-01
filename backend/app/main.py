from fastapi import APIRouter, FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.auth import get_current_user
from app.profile import router as profile_router
from app.database.db import SalesDB
from app.routers import upload_excel
from app.routers import upload_incentive
from app.auth import router as auth_router
from app.routers import dashboard
from app.routers import leaderboard

app = FastAPI(debug=True)

# CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],  # Or use ["*"] during dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Create tables if not already present (but don't populate)
with SalesDB() as db:
    pass  # This ensures tables are created at app startup

# Auth-protected route to fetch performance for logged-in user
@app.get("/performance")
def get_performance(current_user: dict = Depends(get_current_user)):
    phone = current_user["phone"]
    with SalesDB() as db:
        user = db.get_records("users", [("phone", "=", phone)])
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        user_id = user[0]["id"]
        data = db.get_records("performance", [("user_id", "=", user_id)])
    return data

# Test route to verify auth and role
@app.get("/protected-route")
def protected_route(current_user: dict = Depends(get_current_user)):
    return {
        "message": f"Hello {current_user['phone']} with role {current_user['role']}"
    }

# Developer test route to see all users (remove in production)
test_router = APIRouter()

@test_router.get("/test/users")
def list_users():
    with SalesDB() as db:
        users = db.get_records("users")
        return users

# Include all routers
app.include_router(auth_router)
app.include_router(profile_router)
app.include_router(upload_excel.router)
app.include_router(upload_incentive.router)
app.include_router(test_router)
app.include_router(dashboard.router)
app.include_router(leaderboard.router)