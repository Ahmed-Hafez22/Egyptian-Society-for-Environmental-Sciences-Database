from libraries import *
from sqlalchemy import event, create_engine, String, inspect
from sqlalchemy.orm import  Mapped, mapped_column, DeclarativeBase, sessionmaker
import DB
import schemas
from SideFunctions import *

app = FastAPI()

# 4. DEPENDENCY FOR DATABASE SESSIONS
# This function will be called for each request that needs a database connection.
def get_db():
    db_session = DB.SessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()

# 5. API ENDPOINT
@app.post("/readExcel/", response_model=List[dict])
async def read_excel(file: UploadFile = File(...), db_session: sessionmaker = Depends(get_db)):
    """
    Reads an Excel file, validates its content, and stores it in the database.
    """
    # Check if the uploaded file is an Excel file
    if not file.filename.endswith((".xlsx", ".xls")):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload an Excel file.")

    try:
        content = await file.read()
        
        # Use a BytesIO object to allow pandas to read the in-memory file content
        dataframe = pd.read_excel(io.BytesIO(content))

        # Convert dataframe to a list of dictionaries
        data = dataframe.to_dict(orient='records')

        # Add each record from the Excel file to the session
        for item in data:
            new_member = DB.Member(
                member_name=item.get('member_name'),
                phone_number=item.get('phone_number', 'Not Provided'),
                reg_date=str(item.get('reg_date')) if item.get('reg_date') else None, # Ensure date is converted to string
                exp_date=str(item.get('exp_date')) if item.get('exp_date') else None, # Ensure date is converted to string
                status=item.get('status', 'Not Provided'),
                member_email=item.get('member_email', 'Not Provided')
            )
            db_session.add(new_member)
        
        # Commit all new members to the database in a single transaction
        db_session.commit()

        return data

    except Exception as e:
        # Print the actual error to the console for debugging
        print(f"An error occurred: {e}")
        # Return a more informative error to the client
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")


@app.post("/Create-Member")
def Create_member(member: schemas.CreateMember ,db_session: sessionmaker = Depends(get_db)):
    try:
        member_data = member.dict()

        reg_date = member_data.get('reg_date')
        if reg_date in ["string", "", "Not Provided"]:
            reg_date = None  # This will trigger the ORM default

        new_member = DB.Member(
            member_name = member_data['member_name'],
            phone_number = member_data.get('phone_number', 'Not Provided'),
            reg_date = member_data.get('reg_date'),
            member_email = member_data.get('member_email', 'Not Provided')
        )
        new_member.phone_number = phone_num_registration(new_member.phone_number)
        new_member.member_email = check_emails(new_member.member_email)
        new_member.reg_date = dates_registration(new_member.reg_date)[0]
        new_member.exp_date = dates_registration(new_member.reg_date)[1]        
        flag = check_duplicates(new_member)
        if flag == True:
            db_session.add(new_member)
            db_session.commit()
            db_session.refresh(new_member)
            return (f"{new_member.member_name} Got added successfully")
        else:
            return (f"{new_member.member_name} Is already in the database")
    except Exception as e:
        print(f"An error occurred: {e}")
        # Return a more informative error to the client
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    
@app.delete("/Delete-Member/{member_id}")
def Delete_member(member_id: int, db_session: sessionmaker = Depends(get_db)):
    try:
        to_be_delted_member = db_session.query(DB.Member).filter(DB.Member.id == member_id).one()
        db_session.delete(to_be_delted_member)
        db_session.commit()
        return (f"Member with ID: {member_id} got deleted")
    except Exception as e:
        print(f"An error has occurred: {e}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.get("/Show-Members", response_model=List[dict])
def show_members(db_session: sessionmaker = Depends(get_db)):
    try:
        unprocessedMembers = db_session.query(DB.Member).all()
        processedMembers = []
        for member in unprocessedMembers:
            member_dict = {
                "id": member.id,
                "member_name": member.member_name,
                "phone_number": member.phone_number,
                "reg_date": member.reg_date,
                "exp_date": member.exp_date,
                "status": member.status,
                "member_email": member.member_email
            }
            processedMembers.append(member_dict)
        return processedMembers
    except Exception as e:
        print(f"An error has occurred: {e}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.get("/Get-Member/{Member_id}")
def get_member(member_id: int, db_session: sessionmaker = Depends(get_db)):
    try:
        wanted_member = db_session.query(DB.Member).filter(DB.Member.id == member_id).one()
        if not wanted_member:
            raise HTTPException(status_code=500, detail="Member isn't the database")
        
        return wanted_member

    except Exception as e:
        print(f"An error has occurred: {e}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    
@app.get("/Search-for-Member/{Member_name}")
def search_for_member(member_name: str, db_session: sessionmaker = Depends(get_db)):
    try:
        potential_members = db_session.query(DB.Member).filter(DB.Member.member_name.like(f"{member_name}%")).all()
        pot_processedMem = []
        for member in potential_members:
            member_dict = {
                "id": member.id,
                "member_name": member.member_name,
                "phone_number": member.phone_number,
                "reg_date": member.reg_date,
                "exp_date": member.exp_date,
                "status": member.status,
                "member_email": member.member_email
            }
            pot_processedMem.append(member_dict)
        return pot_processedMem
    except Exception as e:
        print(f"An error has occurred: {e}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    
@app.put("/Update-Member/{Member_id}")
def update_member(member_id: int, member: schemas.UpdateMember, db_session: sessionmaker = Depends(get_db)):
    try:
        member_data = member.dict()
        wanted_member = db_session.query(DB.Member).filter(DB.Member.id == member_id).one()
        if member_data['member_name'] != "string":
            wanted_member.member_name = member_data['member_name']

        else:
            pass

        if member_data['phone_number'] != "string":
            wanted_member.phone_number = member_data['phone_number']
        else:
            pass
        
        if member_data['reg_date'] != "string":
            wanted_member.reg_date = member_data['reg_date']
        else:
            pass

        if member_data['member_email'] != "string":
            wanted_member.member_email = member_data['member_email']
        else:
            pass
        db_session.commit()
        db_session.refresh(wanted_member)
        return wanted_member
    except Exception as e:
        print(f"An error has occurred: {e}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")