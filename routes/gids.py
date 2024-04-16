import inspect

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from functions.gids import all_gids, add_gid, update_gid, delete_gid
from db import get_db
from schemas.users import UserCurrent
from routes.auth import get_current_active_user
from schemas.gids import GidCreate, GidUpdate

gid_router = APIRouter()


@gid_router.get("", status_code=200)
async def get_all_gid(search: str = None, status: bool = None, page: int = 1, limit: int = 20,
                        db: Session = Depends(get_db), ):
    return all_gids(search=search, status=status,  page=page, limit=limit, db=db)


@gid_router.post("/add")
async def gid_add(form: GidCreate, db: Session = Depends(get_db),current_gid: UserCurrent = Depends(
    get_current_active_user)):
    if add_gid(form=form,user=current_gid,db=db):
        raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@gid_router.put("/update")
async def gid_update(form: GidUpdate, db: Session = Depends(get_db), current_gid: UserCurrent = Depends(
    get_current_active_user)):
    return update_gid(form=form,user=current_gid, db=db)


@gid_router.delete("/delete")
async def gid_delete(id: int, db: Session = Depends(get_db), current_gid: UserCurrent = Depends(
    get_current_active_user)):
    return delete_gid(id=id, db=db)