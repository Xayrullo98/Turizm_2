from fastapi import HTTPException
from sqlalchemy.orm import joinedload

from models.hotels import Hotels
from utils.pagination import pagination


def all_hotels(search, status, page, limit, db):
    hotels = db.query(Hotels)
    if search:
        search_formatted = "%{}%".format(search)
        hotels = hotels.filter(
            Hotels.title.ilike(search_formatted))
    if status in [True, False]:
        hotels = hotels.filter(Hotels.status == status)

    hotels = hotels.order_by(Hotels.id.desc())
    return pagination(hotels, page, limit)


def one_hotels(db, id):
    hotels = db.query(Hotels).filter(Hotels.id == id).first()
    if hotels:
        return hotels
    raise HTTPException(status_code=400, detail="Bunday ma'lumot mavjud emas")


def add_hotels(title,address, user, db):
    new_hotels = Hotels(
        title=title,
        address=address,
        user_id=user.id

    )
    db.add(new_hotels)
    db.commit()
    return new_hotels


def update_hotels(id,title,address, user, db):
    one_hotels(db=db, id=id)
    db.query(Hotels).filter(Hotels.id == id).update({
        Hotels.title:title,
        Hotels.address:address,
        Hotels.user_id: user.id,

    }

    )
    db.commit()
    raise HTTPException(status_code=200, detail=f"Amaliyot muvaffaqiyatli bajarildi")


def delete_hotels(id, db):
    one_hotels(db=db, id=id)
    db.query(Hotels).filter(Hotels.id == id).update({
        Hotels.status: False, })
    db.commit()
    raise HTTPException(status_code=200, detail=f"Amaliyot muvaffaqiyatli bajarildi")