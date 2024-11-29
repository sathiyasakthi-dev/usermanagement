from pydantic import BaseModel, EmailStr
from uuid import uuid4
from datetime import datetime

class UserModel(BaseModel):
    user_id: str = str(uuid4())
    user_name: str
    user_email: EmailStr
    mobile_number: str
    password: str
    last_update: datetime = datetime.now()
    created_on: datetime = datetime.now()

class NoteModel(BaseModel):
    note_id: str = str(uuid4())
    user_id: str
    note_title: str
    note_content: str
    last_update: datetime = datetime.now()
    created_on: datetime = datetime.now()
