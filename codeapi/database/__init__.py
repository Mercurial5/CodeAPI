from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, Session, sessionmaker

from codeapi.config import PostgresConfig

Base = declarative_base()
engine = create_engine(PostgresConfig.get_connection())

from codeapi.database.models import *


class PostgresDatabase:
    session = None

    def __init__(self):
        if self.session:
            raise Exception('This class is a singleton!')

        self.session: Session = sessionmaker(bind=engine)()

    def __enter__(self):
        if self.session is None:
            self.__init__()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()
        self.session = None
