from libraries import *
from sqlalchemy import event, create_engine, String, inspect
from sqlalchemy.orm import  Mapped, mapped_column, DeclarativeBase, sessionmaker
import DB
import schemas

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
                phone_number=item.get('phone_number'),
                reg_date=str(item.get('reg_date')), # Ensure date is converted to string
                exp_date=str(item.get('exp_date')), # Ensure date is converted to string
                status=item.get('status'),
                member_email=item.get('member_email')
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


@app.post("/Create-Member", response_model= schemas.Member)
def Create_member(member: schemas.CreateMember ,db_session: sessionmaker = Depends(get_db)):
    try:
        new_member = DB.Member(**member.dict())
        db_session.add(new_member)
        db_session.commit()
        db_session.refresh(new_member) 
        return type(new_member)
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