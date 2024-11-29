from fastapi import APIRouter, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from utils.hash import hash_password, verify_password
from utils.auth import create_access_token
from datetime import timedelta

router = APIRouter()

# Connect to MongoDB
db_client = AsyncIOMotorClient("mongodb://localhost:27017")
db = db_client["project"]

@router.post("/register")
async def register_user(user: dict):
    user['password'] = hash_password(user['password'])
    existing_user = await db.users.find_one({"user_email": user["user_email"]})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already exists")
    await db.users.insert_one(user)
    return {"msg": "User registered successfully"}

@router.post("/login/")
async def login(user: dict):
    stored_user = await db.users.find_one({"user_email": user["user_email"]})
    if not stored_user or not verify_password(user["password"], stored_user["password"]):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    token = create_access_token({"sub": stored_user["user_email"]}, timedelta(minutes=15))
    return {"access_token": token, "token_type": "bearer"}

@router.post("/notes/")
async def add_note(note: dict):
    """
    Add a note to the database.
    This endpoint does not require authentication.
    """
    # Insert the note into the "notes" collection
    result = await db.notes.insert_one(note)
    if result.inserted_id:
        return {"msg": "Note added successfully", "note_id": str(result.inserted_id)}
    else:
        raise HTTPException(status_code=500, detail="Failed to add note")
