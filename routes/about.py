import inspect
import json
import shutil
import typing
import requests
from fastapi.security import APIKeyQuery

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from functions.about import all_about, add_about, update_about, delete_about
from db import get_db
from schemas.texts import textsBase, textsUpdate
from utils.config import *

from routes.auth import get_current_active_user
from schemas.users import UserCurrent
from functions.texts import add_text, update_text, text_delete
from functions.pictures import add_picture, update_picture, picture_delete
from functions.videos import add_video, update_video, video_delete
from schemas.videos import videosBase, videosUpdate
from schemas.about import AboutBase
about_router = APIRouter()


@about_router.get("", status_code=200)
async def about_all(
        language: typing.Literal[UZB_LANG, ENG_LANG, RUS_LANG],
        search: str = None,
        status: bool = None,
        page: int = 1, limit: int = 20,
        db: Session = Depends(get_db)):
    return all_about(search=search, status=status, page=page, limit=limit,
                     db=db, language=language)


@about_router.post("/add", )
async def about_add(
        data: str,
        files: typing.Optional[typing.List[UploadFile]] = File(None),
        picture_comments:str=None,
    db: Session = Depends(get_db), current_user: APIKeyQuery = Depends(
            get_current_active_user)):
    new_about = add_about(user=current_user, db=db, )

    if files:
        for file in files:
            with open("media/" + file.filename, 'wb') as image:
                shutil.copyfileobj(file.file, image)
            url = str('media/' + file.filename)
            add_picture(source_id=new_about.id, source=ABOUT, picture_url=url, name=file.filename,
                        user=current_user, db=db)
    # full data json
    try:
        full_data = dict(json.loads(data))
    except Exception as x:
        raise HTTPException(status_code=422, detail=f"data noto'g'ri yuborildi : {x}")

    texts = (full_data.get('texts'))
    videos = (full_data.get('videos'))
    if texts:
        for text in texts:
            add_text(text=text.get('text'), source_id=new_about.id, source=ABOUT, language=text.get("language"),
                     user=current_user,
                     db=db)
    # picture comments texts
    try:
        comment_texts = dict(json.loads(picture_comments))
    except Exception as x:
        raise HTTPException(status_code=422, detail=f"data noto'g'ri yuborildi : {x}")
    comments = (comment_texts.get('texts'))

    if comments:
        for text in comments:
            add_text(text=text.get('text'), source_id=new_about.id, source=PICTURE_COMMENT, language=text.get("language"),
                     user=current_user,
                     db=db)
    if videos:
        for video in videos:
            add_video(name='d', source_id=new_about.id, source=ABOUT, video_url=video.get('text'), user=current_user, db=db)

    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@about_router.put("/update")
async def about_update(
        id: int,
        texts: typing.Optional[typing.List[textsBase]] = None,
        videos: typing.Optional[typing.List[videosBase]] = None,
        files: typing.Optional[typing.List[UploadFile]] = File(None), db: Session = Depends(get_db),
        current_user: UserCurrent = Depends(
            get_current_active_user)):
    if files:
        for file in files:
            with open("media/" + file.filename, 'wb') as image:
                shutil.copyfileobj(file.file, image)
            url = str('media/' + file.filename)
            update_picture(source_id=id, source=ABOUT, image_url=url, user=current_user, db=db)

    if texts:
        for text in texts:
            update_text(text=text.text, source_id=id, source=ABOUT, language=text.language, user=current_user,
                        db=db,id=id)
    if videos:
        for video in videos:
            update_video( source_id=id, source=ABOUT, video_url=video.text, user=current_user, db=db)

    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@about_router.delete("/delete")
async def about_delete(id: int, db: Session = Depends(get_db), current_user: UserCurrent = Depends(
    get_current_active_user)):
    video_delete(source_id=id, source=ABOUT, db=db)
    picture_delete(source_id=id, source=ABOUT, db=db)
    text_delete(source_id=id, source=ABOUT, db=db)
    delete_about(id=id, db=db)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")
