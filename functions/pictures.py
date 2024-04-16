from fastapi import HTTPException
import os
from functions.users import one_user
from models.pictures import Pictures
from utils.pagination import pagination


def all_pictures(search, source_id, source, page, limit, db):
    if search:
        search_formatted = "%{}%".format(search)
        search_filter = Pictures.source.like(search_formatted)
    else:
        search_filter = Pictures.id > 0

    if source_id:
        source_id_filter = Pictures.source_id == source_id
    else:
        source_id_filter = Pictures.user_id > 0

    if source:
        source_filter = Pictures.source == source
    else:
        source_filter = Pictures.id > 0

    pictures = db.query(Pictures).filter(search_filter, source_filter,
                                         source_id_filter).order_by(
        Pictures.id.desc())

    if page and limit:
        return pagination(pictures, page, limit)
    else:
        return pictures.all()


def one_pictures(id, db):
    return db.query(Pictures).filter(Pictures.id == id).first()


def one_picture_via_source_id(source_id, source, db):
    return db.query(Pictures).filter(Pictures.source == source, Pictures.source_id == source_id).first()


def add_picture(name, source_id, source, picture_url, user, db):
    new_pictures_db = Pictures(
        name=name,
        image_url=picture_url,
        source_id=source_id,
        source=source,
        user_id=user.id,

    )
    db.add(new_pictures_db)
    db.commit()
    db.refresh(new_pictures_db)
    return {"data": "Added"}


def update_picture(source_id, source, image_url, user, db):
    picture_delete(source_id=source_id,source=source,db=db)
    db.query(Pictures).filter(Pictures.source_id == source_id, source=source).update({

        Pictures.image_url: image_url,
        Pictures.source_id: source_id,
        Pictures.source: source,
        Pictures.user_id: user.id,
    })
    db.commit()
    return one_pictures(id, db)


def picture_delete(source_id, source, db):
    picture = one_picture_via_source_id(source_id=source_id, source=source, db=db)
    if picture:
        try:
            os.unlink(picture.image_url)
            db.query(Pictures).filter(Pictures.id == picture.id).delete()
            db.commit()
        except Exception:
            pass
        return {"data": "Ma'lumot o'chirildi !"}
