from pydantic import BaseModel

class Blog(BaseModel):
    title: str
    body: str

class ShowBlog(Blog):
    ## this worked even without the below config
    class Config():
        orm_mode = True