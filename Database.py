from libraries import *

# ----------------------
con = connect("Catrina.db")
cur = con.cursor()
# ----------------------
cur.execute(
    """CREATE TABLE IF NOT EXISTS members_info(
    id INTEGER PRIMARY KEY,
    member_name TEXT COLLATE NOCASE,
    phone_number TEXT,
    registration_date TEXT,
    expiration_date TEXT,
    status TEXT,
    email TEXT 
    )"""
)
# ----------------------
con.commit()
