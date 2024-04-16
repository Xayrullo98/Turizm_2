import shutil
import typing

from fastapi import APIRouter, Depends, HTTPException, UploadFile
from sqlalchemy.orm import Session
from functions.texts import all_texts, add_text, update_text, text_delete
from db import get_db
from schemas.texts import textsBase,textsUpdate
from schemas.users import UserCurrent
from routes.auth import get_current_active_user

from utils.config import *

text_router = APIRouter()


@text_router.get("", status_code=200)
async def get_all_text(search: str = None, source: str = None, source_id: int = 0,language:str=None, page: int = 1, limit: int = 20,
                        db: Session = Depends(get_db), ):
    return all_texts(search=search, source_id=source_id,source=source, language=language, page=page, limit=limit, db=db)


@text_router.post("/add")
async def text_add(
        source_id:int,
        source: typing.Literal[HOTELS, NEWS, ABOUT],
        texts: typing.Optional[typing.List[textsBase]] = None,current_user: UserCurrent = Depends(
    get_current_active_user), db: Session = Depends(get_db)):
    if texts:
        for text in texts:
            add_text(source_id=source_id, source=source, text=text.text, language=text.language,
                                user=current_user, db=db)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@text_router.put("/update")
async def text_update(
        source_id:int,
        source: typing.Literal[HOTELS, NEWS, ABOUT],
        texts: typing.Optional[typing.List[textsUpdate]] = None,current_user: UserCurrent = Depends(
    get_current_active_user), db: Session = Depends(get_db)):
    if texts:
        for text in texts:

            update_text(id=text.id,source_id=source_id, source=source, text=text.text, language=text.language,
                                user=current_user, db=db)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@text_router.delete("/delete")
async def delete_text(id: int, db: Session = Depends(get_db), current_text: UserCurrent = Depends(
    get_current_active_user)):
    return text_delete(id=id, db=db)