# from fastapi import APIRouter, Depends, HTTPException
# from motor.motor_asyncio import AsyncIOMotorClient
# from utils.auth import decode_token

# router = APIRouter()

# db_client = AsyncIOMotorClient("mongodb://localhost:27017")
# db = db_client.mydatabase

# async def get_current_user(token: str):
#     payload = decode_token(token)
#     if not payload:
#         raise HTTPException(status_code=401, detail="Invalid token")
#     return await db.users.find_one({"user_email": payload["sub"]})

# @router.post("/notes/")
# async def create_note(note: dict, user=Depends(get_current_user)):
#     note["user_id"] = user["user_id"]
#     await db.notes.insert_one(note)
#     return {"msg": "Note created"}

# @router.get("/notes/")
# async def list_notes(user=Depends(get_current_user)):
#     notes = await db.notes.find({"user_id": user["user_id"]}).to_list(length=100)
#     return notes

# from fastapi import APIRouter, Depends, HTTPException
# from motor.motor_asyncio import AsyncIOMotorClient
# from utils.auth import decode_token
# from uuid import uuid4
# from datetime import datetime

# router = APIRouter()

# # MongoDB Connection
# db_client = AsyncIOMotorClient("mongodb://localhost:27017")
# db = db_client.mydatabase  # Replace "mydatabase" with your database name

# # Dependency to get the current user
# async def get_current_user(token: str):
#     payload = decode_token(token)
#     if not payload:
#         raise HTTPException(status_code=401, detail="Invalid token")
#     user = await db.users.find_one({"user_email": payload["sub"]})
#     if not user:
#         raise HTTPException(status_code=401, detail="User not found")
#     return user

# # Create a new note
# @router.post("/notes/")
# async def create_note(note: dict, user=Depends(get_current_user)):
#     note_id = str(uuid4())  # Generate a unique note ID
#     new_note = {
#         "note_id": note_id,
#         "user_id": user["user_id"],
#         "note_title": note["note_title"],
#         "note_content": note["note_content"],
#         "created_on": datetime.utcnow(),
#         "last_update": datetime.utcnow()
#     }
#     await db.notes.insert_one(new_note)
#     return {"msg": "Note created", "note_id": note_id}

# Get all notes for the current user
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient
from utils.auth import decode_token

router = APIRouter()

db_client = AsyncIOMotorClient("mongodb://localhost:27017")
db = db_client.mydatabase

# Define Pydantic model for the Note
class Note(BaseModel):
    note_title: str
    note_content: str

# Authentication dependency
async def get_current_user(token: str):
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = await db.users.find_one({"user_email": payload["sub"]})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Create a note
@router.post("/notes/")
async def create_note(note: Note, user=Depends(get_current_user)):
    print("Incoming data:", note)
    note_data = note.dict()
    note_data["user_id"] = user["user_id"]
    await db.notes.insert_one(note_data)
    return {"msg": "Note created successfully"}






@router.get("/notes/")
async def list_notes(user=Depends(get_current_user)):
    notes = await db.notes.find({"user_id": user["user_id"]}).to_list(length=100)
    return notes

# Update a note
@router.put("/notes/{note_id}")
async def update_note(note_id: str, update_data: dict, user=Depends(get_current_user)):
    note = await db.notes.find_one({"note_id": note_id, "user_id": user["user_id"]})
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    update_data["last_update"] = datetime.utcnow()
    await db.notes.update_one(
        {"note_id": note_id, "user_id": user["user_id"]},
        {"$set": update_data}
    )
    return {"msg": "Note updated"}

# Delete a note
@router.delete("/notes/{note_id}")
async def delete_note(note_id: str, user=Depends(get_current_user)):
    result = await db.notes.delete_one({"note_id": note_id, "user_id": user["user_id"]})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Note not found")
    return {"msg": "Note deleted"}
