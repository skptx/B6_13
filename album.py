import datetime
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


DB_PATH = "sqlite:///albums.sqlite3"
Base = declarative_base()


class Album(Base):
    __tablename__ = "album"
    id = sa.Column(sa.INTEGER, primary_key=True)
    year = sa.Column(sa.INTEGER)
    artist = sa.Column(sa.TEXT)
    genre = sa.Column(sa.TEXT)
    album = sa.Column(sa.TEXT)


def connect_db():
    engine = sa.create_engine(DB_PATH)
    Base.metadata.create_all(engine)
    session = sessionmaker(engine)
    return session()


def find(artist):
    session = connect_db()
    albums = session.query(Album).filter(Album.artist == artist).all()
    return albums

def findFirst(artist, album, year):
    session = connect_db()
    albums = session.query(Album).filter(Album.artist == artist).filter(Album.album == album).filter(Album.year == year).first()
    return albums

def new(albumData):
    album = Album(year=albumData["year"], artist=albumData["artist"], genre=albumData["genre"], album=albumData["album"])
    session = connect_db()
    session.add(album)
    session.commit()
    return album

# Функция валидации данных. Реализованно 3 проверки, год не число, год больше текушей даты, год меньше нуля
def validate(albumData):
    result = ""
    try:
        intYear = int(albumData["year"])
    except Exception:
        result = "Год альбома задан неверно"
    else:
        now = datetime.datetime.now()
        if intYear > now.year:
            result = "Год альбома не может превышать текущий год"    
        if intYear < 0:
            result = "Год альбома не может быть меньше  нуля"    

    return result
