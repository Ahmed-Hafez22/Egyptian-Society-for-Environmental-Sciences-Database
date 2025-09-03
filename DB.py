from libraries import *
from sqlalchemy import event, create_engine, String, inspect
from sqlalchemy.orm import  Mapped, mapped_column, DeclarativeBase, sessionmaker
from sqlalchemy import inspect

SQLALCHEMY_DATABASE_URL = "sqlite:///./ESES.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    # This argument is required for SQLite to allow multithreading, which FastAPI uses.
    connect_args={"check_same_thread": False}
)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Define a base class for declarative models
class Base(DeclarativeBase):
    pass

DateForamt = "%d %m %Y"

def get_current_date() -> str:
    date_str = datetime.now().strftime(DateForamt)
    return date_str

def get_default_exp_date() -> str:
    return (timedelta(days = 365) + datetime.now()).strftime(DateForamt)


# 2. DEFINE THE ORM MODEL
# Use names that match your Excel columns.
class Member(Base):
    __tablename__ = "members"  # Use a simple, consistent table name

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

@event.listens_for(Member, 'before_insert')
def calculate_expiration_set_status(mapper, connection, target):
    exp_date_obj = None
    if not target.reg_date:
        target.reg_date = get_current_date()

    if target.exp_date and target.exp_date != "Not Provided":
        try:
            exp_date_obj = datetime.strptime(str(target.exp_date), DateForamt)
        except(ValueError,TypeError):
            exp_date_obj = None
            
    if not (target.exp_date or target.exp_date == "Not Provided") and target.reg_date and target.reg_date != "Not Provided":
        try:
            reg_date_obj = datetime.strptime(str(target.reg_date), DateForamt)
            target.reg_date = reg_date_obj.strftime(DateForamt)
            exp_date_obj = reg_date_obj + timedelta(days=365)
            target.exp_date = exp_date_obj.strftime(DateForamt)

        except(ValueError,TypeError):
            target.exp_date = get_default_exp_date()
    
    if exp_date_obj:
        today = datetime.today().date()

        if exp_date_obj.date() >= today:
            target.status = "Active"
        else:
            target.status = "Inactive"
    elif not target.status or target.status == "Not Provided":
        target.status = "Not Provided"        

# Create the database table (if it doesn't exist)
Base.metadata.create_all(bind=engine)
