import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, DateTime, create_engine

DB_LOCATION = 'images.db'

Base = declarative_base()

engine = create_engine('sqlite:///{}'.format(DB_LOCATION))
Session = sessionmaker(bind=engine)

session = Session()


class Image(Base):
    __tablename__ = 'images'

    id = Column(Integer, primary_key=True)
    url = Column(String)
    timestamp = Column(DateTime)
    ext = Column(String)


def url_is_dupe(url):
    if session.query(Image).filter(Image.url == url).count() > 0:
        return True

    return False


def add_image(timestamp, url, ext):
    im = Image(url=url, timestamp=timestamp, ext=ext)
    session.add(im)
    session.commit()
    return im.id
