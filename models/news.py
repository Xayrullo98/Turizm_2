from operator import and_

from sqlalchemy import Column, Integer, String, Boolean, Float, Text, DateTime, func
from sqlalchemy.orm import relationship, backref
from db import Base


class News(Base):
    __tablename__ = "News"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    status = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), default=func.now())

    # shop = relationship('Shop', foreign_keys=[source_id],
    #                     backref=backref('shop_image', order_by="desc(Pictures.id)"),
    #                     primaryjoin=lambda: and_(Shop.id == Pictures.source_id, Pictures.source == "shop"))
