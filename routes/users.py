import inspect

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from functions.users import all_users, add_user, update_user, delete_user
from db import get_db

from routes.auth import get_current_active_user
from schemas.users import UserCreate, UserUpdate, UserCurrent

user_router = APIRouter()


@user_router.get("", status_code=200)
async def get_all_user(search: str = None, status: bool = None, roll: str = None, page: int = 1, limit: int = 20,
                        db: Session = Depends(get_db), current_user: UserCurrent = Depends(
            get_current_active_user)):
    return all_users(search=search, status=status, roll=roll, page=page, limit=limit, db=db)


@user_router.post("/add")
async def user_add(form: UserCreate, db: Session = Depends(get_db)):
    if add_user(form=form, db=db):
        raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@user_router.put("/update")
async def user_update(form: UserUpdate, db: Session = Depends(get_db), current_user: UserCurrent = Depends(
    get_current_active_user)):
    return update_user(form=form, db=db)


@user_router.delete("/delete")
async def user_delete(id: int, db: Session = Depends(get_db), current_user: UserCurrent = Depends(
    get_current_active_user)):
    return delete_user(id=id, db=db)