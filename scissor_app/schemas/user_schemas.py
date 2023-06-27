from pydantic import BaseModel


class UserBase(BaseModel):
    password: str


class UserLoginSchema(UserBase):
    user_id: str


class UserSignupSchema(UserBase):
    username: str
    email_address: str
