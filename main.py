from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from starlette.requests import Request
from starlette.responses import Response, JSONResponse

app = FastAPI()


@app.get("/")
def root():
    return Response(content="Hello world!", status_code=200, media_type="text/plain")
