from pydantic import BaseModel


class CompanyRegistrationSchema(BaseModel):
    email: str
    password: str
    name: str


class UserRegistrationSchema(BaseModel):
    email: str
    password: str
    first_name: str
    last_name: str
