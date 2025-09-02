from libraries import *
import Database

Database.Base.metadata.create_all(bind=Database.engine)

app = FastAPI()

def get_db():
    db = Database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/readExcel", response_model=List[dict])
async def read_excel(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        content = await file.read()
        dataframe = pd.read_excel(io.BytesIO(content))
        data = dataframe.to_dict(orient= 'records')
        for member in data:
            new_member = Database.Member(
                member_name = member.get('member_name'),
                phone_number = member.get('phone_number'),
                reg_date = str(member.get('reg_date')), # Ensure date is converted to string
                exp_date = str(member.get('exp_date')), # Ensure date is converted to string
                status = member.get('status'),
                member_email = member.get('member_email')
            )
            db.add(new_member)
        db.commit()
        return data
    except Exception as e:
         # It's much better to see the actual error than to hide it.
        # This will help you debug future problems.
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing file: {e}")