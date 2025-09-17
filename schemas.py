from libraries import *


class CreateMember(BaseModel):
    member_name: str
    phone_number: Optional[str] = "Not Provided"
    reg_date: Optional[str] = None
    member_email: Optional[str] = "Not Provided"

class Member(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    member_name: str
    phone_number: str
    reg_date: str
    exp_date: str
    status: str
    member_email: str

class UpdateMember(BaseModel):
    member_name: Optional [str] = None
    phone_number: Optional [str] = None
    reg_date: Optional [str] = None
    member_email: Optional [str] = None
    
class Config:
    orm_mode = True