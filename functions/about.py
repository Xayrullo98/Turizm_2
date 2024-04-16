from fastapi import HTTPException
from sqlalchemy.orm import joinedload

from models.about import About
from models.texts import Texts
from utils.pagination import pagination


def all_about(search, status,language, page, limit, db):
    about = db.query(About).join(About.about_text)
    if search:
        search_formatted = "%{}%".format(search)
        about = about.filter(
            About.id.ilike(search_formatted))
    if status in [True, False]:
        about = about.filter(About.status == status)

    about = about.order_by(About.id.desc())
    return pagination(about, page, limit)


def one_about(db, id):
    about = db.query(About).filter(About.id == id).first()
    if about:
        return about
    raise HTTPException(status_code=400, detail="Bunday ma'lumot mavjud emas")


def add_about( user, db):
    new_about = About(
        user_id=user.id

    )
    db.add(new_about)
    db.commit()
    return new_about


def update_about(id,created_at, user, db):
    one_about(db=db, id=id)
    db.query(About).filter(About.id == id).update({
        About.created_at:created_at,
        About.user_id: user.id,

    }

    )
    db.commit()
    raise HTTPException(status_code=200, detail=f"Amaliyot muvaffaqiyatli bajarildi")


def delete_about(id, db):
    one_about(db=db, id=id)
    db.query(About).filter(About.id == id).update({
        About.status: False, })
    db.commit()
    raise HTTPException(status_code=200, detail=f"Amaliyot muvaffaqiyatli bajarildi")