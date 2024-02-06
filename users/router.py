from typing import Annotated, Optional, List
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Response, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from starlette.routing import Route, Mount

from database import get_db
from users.schemas import UserCreate, UserDisplay, UserCreateDB
from users import crud
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from users.auth import Token, authenticate_user, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES, get_password_hash, \
    get_current_user, OAuth2PasswordBearerWithCookie
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from starlette.applications import Starlette

router = APIRouter(
    prefix="/user",
    responses={404: {"description": "Not found"}},
)

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

templates = Jinja2Templates(directory=str(Path(BASE_DIR, 'templates')))

login_required = Annotated[dict, Depends(get_current_user)]


@router.get("/auth/register", response_class=HTMLResponse)
def login_get(request: Request):
    context = {
        "request": request,
    }
    return templates.TemplateResponse(request=request, name="register.html", context=context)


@router.post("auth/register", response_model=UserDisplay)
async def signup(
        user: Annotated[UserCreate, Depends()], db: Session = Depends(get_db)
):
    if crud.get_user(db, user.username):
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="username not available")
    if crud.get_user_by_email(db, user.email):
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="email not available")

    db_user: UserCreateDB = UserCreateDB(username=user.username, first_name=user.first_name, last_name=user.last_name,
                                         email=user.email, pass_hash=get_password_hash(user.raw_password))
    crud.create_user(db, db_user)
    return RedirectResponse(url="/user/auth/login", status_code=status.HTTP_303_SEE_OTHER)


@router.post("/token", response_model=Token)
async def login_for_access_token(response: Response,
                                 form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                                 session: Session = Depends(get_db)
                                 ):
    user = authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    response.set_cookie(key="access_token", value=f"Bearer {access_token}",
                        httponly=True)  # set HttpOnly cookie in response
    return Token(access_token=access_token, token_type="bearer")


@router.get("/auth/login", response_class=HTMLResponse)
def login_get(request: Request):
    context = {
        "request": request,
    }
    return templates.TemplateResponse(request=request, name="login.html", context=context)


@router.post("/auth/login", response_class=HTMLResponse)
async def login_post(request: Request, form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                     session: Session = Depends(get_db)):
    try:
        response = RedirectResponse("/user/home", status_code=status.HTTP_303_SEE_OTHER)
        await login_for_access_token(response=response, session=session, form_data=form_data)
        return response
    except HTTPException as e:
        context = {
            "request": request,
            "errors": {e.detail}
        }

        return templates.TemplateResponse(name="login.html", request=request, context=context)


@router.get("/auth/logout", response_class=HTMLResponse)
def logout_get():
    response = RedirectResponse(url="/user/auth/login")
    response.delete_cookie("access_token")
    return response


@router.get("/myCheck", response_model=UserDisplay)
async def check_user(user: login_required):
    return user


@router.get("/home", response_class=HTMLResponse)
def home(request: Request, user: login_required):
    context = {
        "user": user,
        "request": request,
    }
    return templates.TemplateResponse("index.html", context)

# @router.get("/{item_id}")
# async def read_item(item_id: str):
#     if item_id not in fake_items_db:
#         raise HTTPException(status_code=404, detail="Item not found")
#     return {"name": fake_items_db[item_id]["name"], "item_id": item_id}
#
#
# @router.put(
#     "/{item_id}",
#     tags=["custom"],
#     responses={403: {"description": "Operation forbidden"}},
# )
# async def update_item(item_id: str):
#     if item_id != "plumbus":
#         raise HTTPException(
#             status_code=403, detail="You can only update the item: plumbus"
#         )
#     return {"item_id": item_id, "name": "The great Plumbus"}
#
