from libraries import *
from sqlalchemy import event, create_engine, String, inspect
from sqlalchemy.orm import  Mapped, mapped_column, DeclarativeBase, sessionmaker
from sqlalchemy import inspect

SQLALCHEMY_DATABASE_URL = "sqlite:///./ESES.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
   
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

DateForamt = "%d %m %Y"

def get_current_date() -> str:
    date_str = datetime.now().strftime(DateForamt)
    return date_str

def get_default_exp_date() -> str:
    return (timedelta(days = 365) + datetime.now()).strftime(DateForamt)

class Member(Base):
    __tablename__ = "members"  

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    member_name: Mapped[str] = mapped_column(String, index=True)
    phone_number: Mapped[str] = mapped_column(String, default="Not Provided")
    reg_date: Mapped[str] = mapped_column(String, default=get_current_date)
    exp_date: Mapped[str] = mapped_column(String, default=get_default_exp_date)
    status: Mapped[str] = mapped_column(String, default="Not Provided")
    member_email: Mapped[str] = mapped_column(String, default="Not Provided")
    def to_tuple(self):
        column_names = [c.key for c in inspect(self).mapper.column_attrs]
        return tuple(getattr(self, name) for name in column_names)     

# Create the database table (if it doesn't exist)
Base.metadata.create_all(bind=engine)
