from libraries import *
from DB import get_current_date


class CreateMember(BaseModel):
    member_name: str
    phone_number: Optional[str] = "Not Provided"
    reg_date: Optional[str] = None
    member_email: Optional[str] = "Not Provided"
    
    @validator('reg_date', pre=True, always=True)
    def validate_reg_date(cls, v):
        print(f"Validating reg_date: '{v}'")  # DEBUG
        if v in ["string", "", "Not Provided"]:
            return None
        return v

class Member(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    member_name: str
    phone_number: str
    reg_date: str
    exp_date: str
    status: str
    member_email: str
    
class Config:
    orm_mode = True