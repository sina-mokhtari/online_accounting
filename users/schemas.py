from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    email: str | None = None
    first_name: str | None = None
    last_name: str | None = None


class UserDisplay(UserBase):
    class Config:
        orm_mode = True


class UserCreate(UserBase):
    raw_password: str

    class Config:
        orm_mode = True


class UserRead(UserBase):
    id: int

    class Config:
        orm_mode = True
