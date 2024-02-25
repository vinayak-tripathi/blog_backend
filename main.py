from fastapi import FastAPI
from models import Blog

app = FastAPI()

@app.get("/")
def index():
    return {"data": "blog Home"}

blogs = list()

# Get all blog
@app.get("/blog")
async def get_blogs(limit=10,published:bool =True, sort: str | None = None):
    if published==True:
        return {"blogs": f'{limit} published blogs from db'}
    elif published==False:
        return {"blogs": f'{limit} unpublished blogs from db'}
    elif published==False:
        return {"blogs": f'{limit} published blogs from db'}

@app.post("/blog")
async def create_blog(blog: Blog):
    return {'data':f'Blog with title {blog.title} created'}

@app.get('/blog/unpublished')
def unpublished():
    return {'data': 'all unpublished blogs'}

# Get single blog
@app.get("/blog/{blog_id}")
async def show(blog_id: int):
    for blog in blogs:
        if blog.id==blog_id:
            return blog
    return {"message": f"No blogs found for id {blog_id}"}


# get comments for blog with id
@app.get('/blog/{id}/comments')
def comments(id: int, limit: int | None = None):
    return {'comments': {'1','2'},'limit':limit}