from sqlalchemy import Column, BIGINT, JSON, UUID
from codeapi.database import Base


class Verdict(Base):
    __tablename__ = 'verdicts'
    id = Column(BIGINT, primary_key=True, autoincrement=True)
    task_id = Column(UUID, unique=True)
    data = Column(JSON)
