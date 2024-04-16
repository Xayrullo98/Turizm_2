from operator import and_

from sqlalchemy import Column, Integer, String, Boolean, Float, Text
from sqlalchemy.orm import relationship, backref
from sqlalchemy_utils import URLType
from db import Base


class Videos(Base):
    __tablename__ = "Videos"
    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=True)
    source_id = Column(Integer, nullable=True)
    source = Column(String(30), nullable=True)
    video_url = Column(String(256), nullable=True)
    user_id = Column(Integer, nullable=False)

    # shop = relationship('Shop', foreign_keys=[source_id],
    #                     backref=backref('shop_image', order_by="desc(Pictures.id)"),
    #                     primaryjoin=lambda: and_(Shop.id == Pictures.source_id, Pictures.source == "shop"))
