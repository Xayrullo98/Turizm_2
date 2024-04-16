import shutil
import typing

from fastapi import APIRouter, Depends, HTTPException, UploadFile
from sqlalchemy.orm import Session
from functions.pictures import all_pictures, add_picture, update_picture, picture_delete
from db import get_db
from schemas.users import UserCurrent
from routes.auth import get_current_active_user

from utils.config import *

picture_router = APIRouter()


@picture_router.get("", status_code=200)
async def get_all_picture(search: str = None, source: str = None, source_id: int = 0, page: int = 1, limit: int = 20,
                        db: Session = Depends(get_db), ):
    return all_pictures(search=search, source_id=source_id,source=source,  page=page, limit=limit, db=db)


@picture_router.post("/add")
async def picture_add(
        source_id:int,
        source: typing.Literal[HOTELS, NEWS, ABOUT],
        files: typing.Optional[typing.List[UploadFile]] = None,current_user: UserCurrent = Depends(
    get_current_active_user), db: Session = Depends(get_db)):
    if files:
        for file in files:
            with open("media/" + file.filename, 'wb') as image:
                shutil.copyfileobj(file.file, image)
            url = str('media/' + file.filename)
            add_picture(source_id=source_id, source=source, picture_url=url, name=file.filename,
                                user=current_user, db=db)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@picture_router.put("/update")
async def picture_update(
        source_id:int,
        source: typing.Literal[HOTELS, NEWS, ABOUT],
        files: typing.Optional[typing.List[UploadFile]] = None,current_user: UserCurrent = Depends(
    get_current_active_user), db: Session = Depends(get_db)):
    if files:
        for file in files:
            with open("media/" + file.filename, 'wb') as image:
                shutil.copyfileobj(file.file, image)
            url = str('media/' + file.filename)
            update_picture(source_id=source_id, source=source, image_url=url, name=file.filename,
                                user=current_user, db=db)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@picture_router.delete("/delete")
async def delete_picture(id: int, db: Session = Depends(get_db), current_picture: UserCurrent = Depends(
    get_current_active_user)):
    return picture_delete(id=id, db=db)