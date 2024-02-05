from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from users.router import router

app = FastAPI()

app.include_router(router)


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return PlainTextResponse(str(exc), status_code=400)
