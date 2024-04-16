import inspect
import shutil
import typing

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from functions.hotels import all_hotels, add_hotels, update_hotels, delete_hotels
from db import get_db
from schemas.texts import textsBase, textsUpdate
from utils.config import *

from routes.auth import get_current_active_user
from schemas.users import UserCurrent
from functions.texts import add_text, update_text, text_delete
from functions.pictures import add_picture, update_picture, picture_delete
from functions.videos import add_video, update_video, video_delete
from schemas.videos import videosBase, videosUpdate

hotels_router = APIRouter()


@hotels_router.get("", status_code=200)
async def hotels_all(
        language: typing.Literal[UZB_LANG, ENG_LANG, RUS_LANG],
        search: str = None,
        status: bool = None,
        page: int = 1, limit: int = 20,
        db: Session = Depends(get_db)):
    return all_hotels(search=search, status=status, page=page, limit=limit,
                     db=db, language=language)


@hotels_router.post("/add")
async def hotels_add(
        title:str,
        address:str,
        texts: typing.Optional[typing.List[textsBase]] = None,
        videos: typing.Optional[typing.List[videosBase]] = None,
        files: typing.Optional[UploadFile] = None
        , db: Session = Depends(get_db), current_user: UserCurrent = Depends(
            get_current_active_user)):
    new_hotels = add_hotels(title=title,address=address,user=current_user, db=db, )

    if files:
        for file in files:
            with open("media/" + file.filename, 'wb') as image:
                shutil.copyfileobj(file.file, image)
            url = str('media/' + file.filename)
            add_picture(source_id=new_hotels.get('id'), source=HOTELS, picture_url=url, name=file.filename,
                        user=current_user, db=db)

    if texts:
        for text in texts:
            add_text(text=text.text, source_id=new_hotels.id, source=HOTELS, language=text.language, user=current_user,
                     db=db)
    if videos:
        for video in videos:
            add_video(name='d', source_id=new_hotels.id, source=HOTELS, video_url=video.text, user=current_user, db=db)

    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@hotels_router.put("/update")
async def hotels_update(
        id: int,
        texts: typing.Optional[typing.List[textsUpdate]] = None,
        videos: typing.Optional[typing.List[videosUpdate]] = None,
        files: typing.Optional[typing.List[UploadFile]] = None, db: Session = Depends(get_db),
        current_user: UserCurrent = Depends(
            get_current_active_user)):
    if files:
        for file in files:
            with open("media/" + file.filename, 'wb') as image:
                shutil.copyfileobj(file.file, image)
            url = str('media/' + file.filename)
            update_picture(source_id=id, source=HOTELS, picture_url=url, name=file.filename,
                           user=current_user, db=db)

    if texts:
        for text in texts:
            update_text(id=text.id,text=text.text, source_id=id, source=HOTELS, language=text.language, user=current_user,
                        db=db)
    if videos:
        for video in videos:
            update_video(id=video.id,name='d', source_id=id, source=HOTELS, video_url=video.text, user=current_user, db=db)

    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@hotels_router.delete("/delete")
async def hotels_delete(id: int, db: Session = Depends(get_db), current_user: UserCurrent = Depends(
    get_current_active_user)):
    video_delete(source_id=id, source=HOTELS, db=db)
    picture_delete(source_id=id, source=HOTELS, db=db)
    text_delete(source_id=id, source=HOTELS, db=db)
    delete_hotels(id=id, db=db)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")
