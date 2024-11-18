from sqlalchemy import create_engine

from utils.conf import Config as conf


class Db:
    DB_USER = conf.db.DB_USER
    DB_NAME = conf.db.DB_NAME
    DB_HOST = conf.db.DB_HOST
    DB_PORT = conf.db.DB_PORT
    DB_PASSWORD = conf.db.DB_PASSWORD
    URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


engine = create_engine(Db.URL)
