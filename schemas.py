from libraries import *


class CreateMember(BaseModel):
    member_name: str
    phone_number: str
    reg_date: str
    exp_date: str
    status: str
    member_email: str
    
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
    