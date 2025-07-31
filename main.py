from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from starlette.requests import Request
from starlette.responses import Response, JSONResponse
import datetime

app = FastAPI()

class PostModel(BaseModel):
    author : str
    title : str
    content : str
    creation_datetime : datetime.datetime

post_list : List[PostModel] = []

def serialized_posts():
    posts_converted = []
    for post in post_list:
        posts_converted.append(post.model_dump())
    return posts_converted

@app.get("/ping")
def root():
    return Response(content="pong", status_code=200, media_type="text/plain")

@app.get("/home")
def home():
    return Response(content="<h1>Welcome home!</h1>", status_code=200, media_type="text/html")

@app.post("/posts")
def new_post(posts: List[PostModel]):
    global post_list
    post_list.extend(posts)
    return JSONResponse({"posts" : [post.model_dump() for post in post_list]}, status_code=201)

@app.get("/posts")
def get_posts():
    return {"posts": serialized_posts()}

@app.put("/posts")
def update_posts(posts: List[PostModel]):
    global post_list
    for new_post in posts:
        found = False
        for i, existing_post in enumerate(post_list):
            if new_post.title == existing_post.title:
                post_list[i] = new_post
                found = True
                break
        if not found:
            post_list.append(new_post)
    return {"posts": serialized_posts()}

@app.get("/{full_path:path}")
def catch_all(full_path: str):
    return Response(content="<p>404 not found</p>", status_code=404, media_type="text/html")