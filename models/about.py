from operator import and_

from sqlalchemy import Column, Integer, String, Boolean, Float, Text, DateTime, func
from sqlalchemy.orm import relationship, backref
from db import Base


class About(Base):
    __tablename__ = "About"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    status = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), default=func.now())
    about_text = relationship('Texts', back_populates="about_context")
    # shop = relationship('Shop', foreign_keys=[source_id],
    #                     backref=backref('shop_image', order_by="desc(Pictures.id)"),
    #                     primaryjoin=lambda: and_(Shop.id == Pictures.source_id, Pictures.source == "shop"))
