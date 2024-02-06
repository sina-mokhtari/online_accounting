from fastapi import FastAPI, HTTPException, status, Depends, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse, RedirectResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from users.router import router

from fastapi.staticfiles import StaticFiles
from pathlib import Path

app = FastAPI()

app.include_router(router)

BASE_DIR = Path(__file__).resolve().parent

app.mount("/assets", StaticFiles(directory=Path(BASE_DIR, "users/templates/assets")), name="static")


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}


@app.exception_handler(HTTPException)
async def unicorn_exception_handler(request, e):
    if e.status_code == status.HTTP_401_UNAUTHORIZED:
        return RedirectResponse(url="/user/auth/login")


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return PlainTextResponse(str(exc), status_code=400)
