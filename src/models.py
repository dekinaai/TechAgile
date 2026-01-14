from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


Base = declarative_base()


class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    description = Column(String(1000), nullable=True)
    status = Column(String(20), default='todo')
    priority = Column(Integer, default=3)
    created_at = Column(DateTime, default=datetime.utcnow)


# engine/session helper for local dev
engine = create_engine('sqlite:///tasks.db')
SessionLocal = sessionmaker(bind=engine)


if __name__ == '__main__':
    Base.metadata.create_all(engine)
