from pydantic import BaseModel
from fastapi import FastAPI, Depends, Form


class UserBase(BaseModel):
    username: str
    email: str | None = None
    first_name: str | None = None
    last_name: str | None = None


def form_body(cls):
    cls.__signature__ = cls.__signature__.replace(
        parameters=[
            arg.replace(default=Form(...))
            for arg in cls.__signature__.parameters.values()
        ]
    )
    return cls


class UserDisplay(UserBase):
    class Config:
        orm_mode = True

@form_body
class UserCreate(UserBase):
    raw_password: str

    class Config:
        orm_mode = True


class UserCreateDB(UserBase):
    pass_hash: str


class UserRead(UserBase):
    id: int

    class Config:
        orm_mode = True
