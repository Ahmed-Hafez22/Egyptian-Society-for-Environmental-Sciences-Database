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

# 2. DEFINE THE ORM MODEL
# Use names that match your Excel columns.
class Member(Base):
    __tablename__ = "members"  # Use a simple, consistent table name

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    member_name: Mapped[str] = mapped_column(String, index=True)
    phone_number: Mapped[str]
    reg_date: Mapped[str]
    exp_date: Mapped[str]
    status: Mapped[str] = mapped_column(default="Not Provided")
    member_email: Mapped[str]
    def to_tuple(self):
        column_names = [c.key for c in inspect(self).mapper.column_attrs]
        return tuple(getattr(self, name) for name in column_names)

@event.listens_for(Member, 'before_insert')
def calculate_expiration_set_status(mapper, connection, target):
    exp_date_obj = None
    DateForamt = "%d %m %Y"
    if target.exp_date:
        try:
            exp_date_obj = datetime.strptime(str(target.exp_date), DateForamt)
        except(ValueError,TypeError):
            exp_date_obj = None
            
    if not target.exp_date and target.reg_date:
        try:
            reg_date_obj = datetime.strptime(str(target.reg_date), DateForamt)
            target.reg_date = reg_date_obj.strftime(DateForamt )
            exp_date_obj = reg_date_obj + timedelta(days=365)
            target.exp_date = exp_date_obj.strftime(DateForamt)
        except(ValueError,TypeError):
            pass
    
    if exp_date_obj:
        today = datetime.today().date()

        if exp_date_obj.date() >= today:
            target.status = "Active"
        else:
            target.status = "Inactive"
    elif not target.status:
        target.status = "Not Provided"        



# Create the database table (if it doesn't exist)
Base.metadata.create_all(bind=engine)
