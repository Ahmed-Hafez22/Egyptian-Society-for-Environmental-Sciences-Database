from libraries import *

def get_current_date():
    return date.today().strftime("%d %m %Y")


class CreateMember(BaseModel):
    member_name: str
    phone_number: Optional[str] = "Not Provided"
    reg_date: str = Field(default_factory=get_current_date())
    exp_date: Optional[str] = "Not Provided"
    status: Optional[str] = "Not Provided"
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
    
class Config:
    orm_mode = True
    