from fastapi import HTTPException
from sqlalchemy.orm import joinedload

from models.users import Users
from routes.auth import get_password_hash
from utils.pagination import pagination


def all_users(search,status, roll, page, limit, db):
    users = db.query(Users)
    if search:
        search_formatted = "%{}%".format(search)
        users = users.filter(
            Users.name.ilike(search_formatted) | Users.username.ilike(search_formatted))

    if roll:
        users = users.filter(Users.roll == roll)
    if status in [True, False]:
        users = users.filter(Users.status == status)

    users = users.order_by(Users.id.desc())
    return pagination(users, page, limit)


def one_user(db, id):
    user = db.query(Users).filter(Users.id == id).first()
    if user:
        return user
    raise HTTPException(status_code=400, detail="Bunday foydalanuvchi mavjud emas")


def add_user(form, db):
    user_verification = db.query(Users).filter(Users.username == form.username).first()
    if user_verification:
        raise HTTPException(status_code=400, detail="Bunday foydalanuvchi mavjud ")
    new_user = Users(
        name=form.name,
        username=form.username,
        roll=form.roll,
        password=get_password_hash(form.password),

    )
    db.add(new_user)
    db.commit()
    return new_user


def update_user(form, db):
    one_user(db=db, id=form.id)
    db.query(Users).filter(Users.id == form.id).update({
        Users.username: form.username,
        Users.name: form.name,
        Users.roll: form.roll,
        Users.password: get_password_hash(form.password),

    }

    )
    db.commit()
    raise HTTPException(status_code=200, detail=f"Amaliyot muvaffaqiyatli bajarildi")


def delete_user(id, db):
    one_user(db=db, id=id)
    db.query(Users).filter(Users.id == id).update({
        Users.status: False, })
    db.commit()
    raise HTTPException(status_code=200, detail=f"Amaliyot muvaffaqiyatli bajarildi")