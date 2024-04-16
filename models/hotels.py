from operator import and_

from sqlalchemy import Column, Integer, String, Boolean, Float, Text, DateTime, func
from sqlalchemy.orm import relationship, backref
from db import Base


class Hotels(Base):
    __tablename__ = "Hotels"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    title = Column(String(100), nullable=True)
    address = Column(String(100), nullable=True)
    status = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), default=func.now())

    # shop = relationship('Shop', foreign_keys=[source_id],
    #                     backref=backref('shop_image', order_by="desc(Pictures.id)"),
    #                     primaryjoin=lambda: and_(Shop.id == Pictures.source_id, Pictures.source == "shop"))
