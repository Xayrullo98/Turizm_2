from operator import and_

from sqlalchemy import Column, Integer, String, Boolean, Float, Text
from sqlalchemy.orm import relationship, backref
from models.hotels import Hotels
from models.news import News
from models.about import About
from utils.config import *
from db import Base


class Texts(Base):
    __tablename__ = "Texts"
    id = Column(Integer, primary_key=True)
    text = Column(Text, nullable=True)
    source_id = Column(Integer, nullable=True)
    source = Column(String(30), nullable=True)
    language = Column(String(30), nullable=True)
    user_id = Column(Integer, nullable=False)

    about_context = relationship('About', foreign_keys=[source_id],
                        backref=backref('about_text', order_by="desc(Texts.id)"),
                        primaryjoin=lambda: and_(About.id == Texts.source_id, Texts.source == ABOUT))

    hotels_context = relationship('Hotels', foreign_keys=[source_id],
                         backref=backref('hotels_text', order_by="desc(Texts.id)"),
                         primaryjoin=lambda: and_(Hotels.id == Texts.source_id, Texts.source == HOTELS))

    news_context = relationship('News', foreign_keys=[source_id],
                          backref=backref('news_text', order_by="desc(Texts.id)"),
                          primaryjoin=lambda: and_(News.id == Texts.source_id, Texts.source == NEWS))
