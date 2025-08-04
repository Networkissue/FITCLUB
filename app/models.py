# app/models.py
from pydantic import BaseModel
from typing import List, Optional

class Meal(BaseModel):
    id: str
    title: str
    description: str
    calories: str
    protein: str
    image: str
    category: str  # "bulking" or "cutting"

class MealCreate(BaseModel):
    title: str
    description: str
    calories: str
    protein: str
    image: str
    category: str

#for userdata
class SignupModel(BaseModel):
    id: str
    username:str
    email: str
    mobile: str
    password: str
    confirm_password: str
    gender:str
    role: str = "user"


# class PaymentRequest(BaseModel):
#     amount: int
#     orderId: str


class SigninModel(BaseModel):
    mobile: str
    password: str
    captcha: str


class User(BaseModel):
    id: str
    name: str
    username: str
    email: str
    mobile: str
    password: str
    gender: str
    role: str
    joining_date: str
    last_payment_date: str
    next_due_date: str
    membership_type: str = "Premium"


class UpdateProfileRequest(BaseModel):
    name: str
    email: str
    mobile: str
    gender: str


class PaymentRecord(BaseModel):
    user_id: str
    last_payment: str
    next_due: str
    status: str


class UpdatePaymentRequest(BaseModel):
    payment_date: str