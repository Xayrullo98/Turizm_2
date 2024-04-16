from fastapi import HTTPException
from sqlalchemy.orm import joinedload

from models.gids import Gids
from routes.auth import get_password_hash
from utils.pagination import pagination


def all_gids(search,status,  page, limit, db):
    gids = db.query(Gids)
    if search:
        search_formatted = "%{}%".format(search)
        gids = gids.filter(
            Gids.name.ilike(search_formatted) | Gids.address.ilike(search_formatted)|
            Gids.phone.ilike(search_formatted)| Gids.languages.ilike(search_formatted))

    
    if status in [True, False]:
        gids = gids.filter(Gids.status == status)

    gids = gids.order_by(Gids.id.desc())
    return pagination(gids, page, limit)


def one_gid(db, id):
    gid = db.query(Gids).filter(Gids.id == id).first()
    if gid:
        return gid
    raise HTTPException(status_code=400, detail="Bunday foydalanuvchi mavjud emas")


def add_gid(form,user, db):

    new_gid = Gids(
        name=form.name,
        phone=form.phone,
        address=form.address,
        languages=form.languages,
        user_id=user.id

    )
    db.add(new_gid)
    db.commit()
    return new_gid


def update_gid(form, user,db):
    one_gid(db=db, id=form.id)
    db.query(Gids).filter(Gids.id == form.id).update({
        Gids.phone: form.phone,
        Gids.name: form.name,
        Gids.address: form.address,
        Gids.languages: form.languages,
        Gids.user_id: user.id,

    }

    )
    db.commit()
    raise HTTPException(status_code=200, detail=f"Amaliyot muvaffaqiyatli bajarildi")


def delete_gid(id, db):
    one_gid(db=db, id=id)
    db.query(Gids).filter(Gids.id == id).update({
        Gids.status: False, })
    db.commit()
    raise HTTPException(status_code=200, detail=f"Amaliyot muvaffaqiyatli bajarildi")