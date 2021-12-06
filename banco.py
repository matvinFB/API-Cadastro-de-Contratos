from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

engine = create_engine("postgresql://playground:dev123456@127.0.0.1/recrutamento")
session = sessionmaker(bind = engine)()
Base = declarative_base()