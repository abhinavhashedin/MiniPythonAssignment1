from http.client import HTTPException
from fastapi import FastAPI,Depends
from datetime import datetime
from typing import List, Union
from fastapi.responses import JSONResponse
from models import User
from database import Base, SessionLocal, engine
from sqlalchemy.orm import Session
from pydantic import BaseModel

app = FastAPI()

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class UserSchema(BaseModel):
    id:int
    user:str
    key:str
    value:Union[str,float,int]
    Tags:List[Union[str, None]]
    created_at:Union[datetime, None]
    updated_at:Union[datetime, None]
    class Config:
       orm_mode=True


@app.get("/api/users", response_model=List[UserSchema])
async def get_users(db: Session=Depends(get_db)):
    return db.query(User).all()


@app.get("/api/users/{key}", response_model=List[UserSchema])
async def get_users_keyname(user: UserSchema,db: Session=Depends(get_db)):
     user_bykey=db.query(User).filter(User.key == user.key) 
     return user_bykey; 


@app.post("/api/users", response_model=UserSchema)
async def get_users(user: UserSchema, db: Session=Depends(get_db)):
 new_user = User(id=user.id, user=user.user, key=user.key,value=user.value,Tags=user.Tags,created_at=user.created_at,updated_at=user.updated_at)
 db.add(new_user)
 db.commit()
 return new_user


@app.put("api/users/{id}",response_model=UserSchema)
async def update_user(id: int,user:UserSchema, db:Session=Depends(get_db)):
 try:
   updated_user=db.query(User).filter(User.id == id).first()
   updated_user.id=user.id
   updated_user.user=user.user
   updated_user.key=user.key
   updated_user.value=user.value
   updated_user.Tags=user.Tags
   updated_user.created_at=user.created_at
   updated_user.updated_at=user.updated_at
   db.add(updated_user)
   db.commit()
   return updated_user
 except:
    return HTTPException(status_code=404,detail="user not found")


@app.delete("/users/{id}",response_class=JSONResponse)
async def delete_user(id:int,db:Session=Depends(get_db)):
 try:
    deleted_user=db.query(User).filter(User.id == id).first()
    db.delete(deleted_user)
    return {""}
 except:
  return HTTPException(status_code=484,detail="user not found")