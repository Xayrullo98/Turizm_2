from fastapi import HTTPException
import os
from models.videos import Videos
from utils.pagination import pagination


def all_videos(search, source_id, source, page, limit, db):
    if search:
        search_formatted = "%{}%".format(search)
        search_filter = Videos.source.like(search_formatted)
    else:
        search_filter = Videos.id > 0

    if source_id:
        source_id_filter = Videos.source_id == source_id
    else:
        source_id_filter = Videos.user_id > 0

    if source:
        source_filter = Videos.source == source
    else:
        source_filter = Videos.id > 0

    videos = db.query(Videos).filter(search_filter, source_filter,
                                         source_id_filter).order_by(
        Videos.id.desc())

    if page and limit:
        return pagination(videos, page, limit)
    else:
        return videos.all()


def one_videos(id, db):
    return db.query(Videos).filter(Videos.id == id).first()


def one_video_via_source_id(source_id, source, db):
    return db.query(Videos).filter(Videos.source == source, Videos.source_id == source_id).first()


def add_video(name, source_id, source, video_url, user, db):
    new_videos_db = Videos(
        name=name,
        video_url=video_url,
        source_id=source_id,
        source=source,
        user_id=user.id,

    )
    db.add(new_videos_db)
    db.commit()
    db.refresh(new_videos_db)
    return {"data": "Added"}


def update_video(source_id, source, video_url, user, db):
    db.query(Videos).filter(Videos.source_id == source_id, source=source).update({

        Videos.video_url: video_url,
        Videos.source_id: source_id,
        Videos.source: source,
        Videos.user_id: user.id,
    })
    db.commit()
    return {"data": "Ma'lumot o'zgartirildi"}


def video_delete(source_id, source, db):
    video = one_video_via_source_id(source_id=source_id, source=source, db=db)
    if video:
        try:
            os.unlink(video.image_url)
            db.query(Videos).filter(Videos.id == video.id).delete()
            db.commit()
        except Exception:
            pass
        return {"data": "Ma'lumot o'chirildi !"}
