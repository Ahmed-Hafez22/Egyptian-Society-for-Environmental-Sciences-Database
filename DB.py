from libraries import *
from sqlalchemy import event, create_engine, String, inspect
from sqlalchemy.orm import  Mapped, mapped_column, DeclarativeBase, sessionmaker
from sqlalchemy import inspect

os.makedirs("database", exist_ok=True)
SQLALCHEMY_DATABASE_URL = "sqlite:///./database/ESES.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={
        "check_same_thread": False,
        "timeout": 30  # Wait 30 seconds if database is locked
    }
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

class Member(Base):
    __tablename__ = "members"  

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    member_name: Mapped[str] = mapped_column(String, index=True)
    phone_number: Mapped[str] = mapped_column(String, default="Not Provided")
    reg_date: Mapped[str] = mapped_column(String, default="Not Provided")
    exp_date: Mapped[str] = mapped_column(String, default="Not Provided")
    status: Mapped[str] = mapped_column(String, default="Not Provided")
    member_email: Mapped[str] = mapped_column(String, default="Not Provided")
    def to_tuple(self):
        column_names = [c.key for c in inspect(self).mapper.column_attrs]
        return tuple(getattr(self, name) for name in column_names)     

# Create the database table (if it doesn't exist)
Base.metadata.create_all(bind=engine)
#Finished