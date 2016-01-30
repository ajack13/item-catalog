# Script to generate database in sqlite using sqlalchemy 
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

''' create User table '''
class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))


''' create Genre table '''
class Genre(Base):
    __tablename__ = 'genre'
   
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    ''' serialize data '''
    @property
    def serialize(self):
        return {
           'name'         : self.name,
           'id'           : self.id,
       }

''' create Albums table '''
class Albums(Base):
    __tablename__ = 'albums'

    name =Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)
    description = Column(String(250))
    price = Column(String(8))
    p_type = Column(String(250))
    genre_id = Column(Integer,ForeignKey('genre.id'))
    genre = relationship(Genre)
    img_name = Column(String(150))
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    ''' serialize data '''
    @property
    def serialize(self):
        return {
           'name'         : self.name,
           'id'           : self.id,
           'description'  : self.description,
           'price'        : self.price,
           'p_type'       : self.p_type,
           'genre_id'     : self.genre_id,
           'img_name'     : self.img_name,
       }



engine = create_engine('sqlite:///music_store.db')
 

Base.metadata.create_all(engine)

