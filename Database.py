from libraries import *

# # ----------------------
# con = connect("ESES.db")
# cur = con.cursor()
# # ----------------------
# cur.execute( #Supposedly can be deleted later on
#     """CREATE TABLE IF NOT EXISTS members_info(
#     id INTEGER PRIMARY KEY,
#     member_name TEXT COLLATE NOCASE,
#     phone_number TEXT,
#     registration_date TEXT,
#     expiration_date TEXT,
#     status TEXT,
#     email TEXT 
#     )"""
# )

SQLALCHEMY_DATABASE_URL = "sqlite:///ESES.db/"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
class Base(DeclarativeBase): pass
class Member(Base):
    __tablename__ = "Members_Information"
    id: Mapped[int] = mapped_column(primary_key=True)
    member_name: Mapped[str] = mapped_column(String)
    phone_number: Mapped[str] = mapped_column(String)
    reg_date: Mapped[str] = mapped_column(String)
    exp_date: Mapped[str] = mapped_column(String)
    status: Mapped[str] = mapped_column(String)
    member_email: Mapped[str] = mapped_column(String)

session = sessionmaker(autocommit= False, autoflush=False, bind = engine)
session = Session()
# ----------------------
# con.commit()

