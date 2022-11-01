from sqlalchemy import Column, Integer, JSON, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from web_app.database import Base
from datetime import datetime


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    email = Column(String(100))
    created = Column(DateTime(), default=datetime.now)
    password = Column(String(100))

    def __init__(self, name=None, email=None, created=None, password=None):
        self.name = name
        self.email = email
        self.created = created
        self.password = password

    def __repr__(self):
        return f'<User {self.name} {self.email}>'


class Request(Base):
    __tablename__ = 'request'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    field_name = Column(String(150))
    region_name = Column(String(150))
    search_name = Column(String(150))
    data = Column(JSON, nullable=True)
    status = Column(Integer)
    created = Column(DateTime(), default=datetime.now)
    updated = Column(DateTime(), default=None)
    user = relationship("User", backref="result")

    def __init__(self, user_id=None, field_name=None, region_name=None, search_name=None,  data=None, status=None,
                 created=None, updated=None,):
        self.user_id = user_id
        self.field_name = field_name
        self.region_name = region_name
        self.search_name = search_name
        self.data = data
        self.status = status
        self.created = created
        self.updated = updated

    def __repr__(self):
        return f'<User {self.search_name} {self.status} {self.created}>'


class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(Text(500))
    email = Column(String(100))
    name = Column(String(100))

    def __init__(self, id=None, name=None, text=None, email=None):
        self.id = id
        self.text = text
        self.email = email
        self.name = name

    def __repr__(self):
        return f'Request {self.id} {self.email} {self.name}'
