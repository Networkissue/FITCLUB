from pydantic import BaseModel

#for userdata
class signup(BaseModel):
    username:str
    email: str
    mobile: int
    gender:str
    Role: str


class PaymentRequest(BaseModel):
    amount: int
    orderId: str


class signInRequest(BaseModel):
    mobile: str
    captcha: str

