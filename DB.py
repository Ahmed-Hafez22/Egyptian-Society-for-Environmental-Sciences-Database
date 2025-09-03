from libraries import *
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
    status: Mapped[str]
    member_email: Mapped[str]
    def to_tuple(self):
        column_names = [c.key for c in inspect(self).mapper.column_attrs]
        return tuple(getattr(self, name) for name in column_names)

# Create the database table (if it doesn't exist)
Base.metadata.create_all(bind=engine)
