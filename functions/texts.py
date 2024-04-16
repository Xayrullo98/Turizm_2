from fastapi import HTTPException
import os
from models.texts import Texts
from utils.pagination import pagination


def all_texts(search, source_id, source, language,page, limit, db):
    if search:
        search_formatted = "%{}%".format(search)
        search_filter = Texts.text.like(search_formatted)
    else:
        search_filter = Texts.id > 0

    if source_id:
        source_id_filter = Texts.source_id == source_id
    else:
        source_id_filter = Texts.user_id > 0

    if language:
        language_filter = Texts.language == language
    else:
        language_filter = Texts.user_id > 0

    if source:
        source_filter = Texts.source == source
    else:
        source_filter = Texts.id > 0

    texts = db.query(Texts).filter(search_filter, source_filter,
                                         source_id_filter,language_filter).order_by(
        Texts.id.desc())

    if page and limit:
        return pagination(texts, page, limit)
    else:
        return texts.all()


def one_texts(id, db):
    return db.query(Texts).filter(Texts.id == id).first()


def one_text_via_source_id(source_id, source, language,db):
    return db.query(Texts).filter(Texts.source == source, Texts.source_id == source_id,language=language).first()


def add_text(text, source_id, source, language, user, db):
    new_texts_db = Texts(
        text=text,
        language=language,
        source_id=source_id,
        source=source,
        user_id=user.id,

    )
    db.add(new_texts_db)
    db.commit()
    db.refresh(new_texts_db)
    return {"data": "Added"}


def update_text(id,language,source_id, source, text, user, db):
    db.query(Texts).filter(Texts.id==id).update({

        Texts.text: text,
        Texts.source_id: source_id,
        Texts.source: source,
        Texts.language: language,
        Texts.user_id: user.id,
    })
    db.commit()
    return {"data": "Ma'lumot o'zgartirildi !"}

def text_delete(source_id, source, db):
    text = one_text_via_source_id(source_id=source_id, source=source, db=db)
    if text:
        try:
            db.query(Texts).filter(Texts.id == text.id).delete()
            db.commit()
        except Exception:
            pass
        return {"data": "Ma'lumot o'chirildi !"}
