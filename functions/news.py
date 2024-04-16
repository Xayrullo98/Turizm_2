from fastapi import HTTPException
from sqlalchemy.orm import joinedload

from models.news import News
from utils.pagination import pagination


def all_news(search, status, page, limit, db):
    news = db.query(News)
    if search:
        search_formatted = "%{}%".format(search)
        news = news.filter(
            News.id.ilike(search_formatted))
    if status in [True, False]:
        news = news.filter(News.status == status)

    news = news.order_by(News.id.desc())
    return pagination(news, page, limit)


def one_news(db, id):
    news = db.query(News).filter(News.id == id).first()
    if news:
        return news
    raise HTTPException(status_code=400, detail="Bunday ma'lumot mavjud emas")


def add_news(creatd_at, user, db):
    new_news = News(
        creatd_at=creatd_at,
        user_id=user.id

    )
    db.add(new_news)
    db.commit()
    return new_news


def update_news(id,created_at, user, db):
    one_news(db=db, id=id)
    db.query(News).filter(News.id == id).update({
        News.created_at:created_at,
        News.user_id: user.id,

    }

    )
    db.commit()
    raise HTTPException(status_code=200, detail=f"Amaliyot muvaffaqiyatli bajarildi")


def delete_news(id, db):
    one_news(db=db, id=id)
    db.query(News).filter(News.id == id).update({
        News.status: False, })
    db.commit()
    raise HTTPException(status_code=200, detail=f"Amaliyot muvaffaqiyatli bajarildi")