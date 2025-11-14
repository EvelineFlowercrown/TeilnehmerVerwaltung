#database.py
from sqlalchemy import create_engine, text, ForeignKey, Integer, String, Date, column
from sqlalchemy.orm import sessionmaker, DeclarativeBase, relationship

#region DB-Setup

# setup engine base string: "<dialect>+<optional_driver>://<username>:<password>@<host>:<port>/<database>"
#alternativ in memory: "sqlite://:memory:"
DATABASE_URL = "sqlite:///Database.db"
engine = create_engine(DATABASE_URL, echo=False)

# setup session
session = sessionmaker(bind=engine)
session = session()

# ORM Base Class
class BaseClass(DeclarativeBase):
    pass

#endregion DB-Setup
