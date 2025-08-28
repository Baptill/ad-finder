from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    role: str | None = None


class UserOut(BaseModel):
    id: int
    username: str
    email: str
    role: str
    model_config = {"from_attributes": True}


class UserLogin(BaseModel):
    email_or_username: str
    password: str


class EmailRequest(BaseModel):
    email: str


class ResetForgetPassword(BaseModel):
    new_password: str
    confirm_password: str


class SuccessMessage(BaseModel):
    success: bool
    status_code: int
    message: str
