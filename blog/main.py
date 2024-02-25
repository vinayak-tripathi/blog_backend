from fastapi import FastAPI, Depends, status, Response, HTTPException
from typing import List

from . import schemas, models
from .hashing import Hash
from .database import SessionLocal, engine
from sqlalchemy.orm import Session

models.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()


@app.post("/blog", 
          status_code = status.HTTP_201_CREATED,
          tags=['Blog'])
def create(blog: schemas.Blog, db : Session = Depends(get_db)):
    # return {'title':blog.title,'body':blog.body}
    new_blog = models.Blog(title = blog.title,
                           body = blog.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.delete("/blog/{id}", 
            status_code = status.HTTP_204_NO_CONTENT,
            tags=['Blog'])
def delete_blog(id: int, db : Session = Depends(get_db)):
    db_blog = db.query(models.Blog).filter(models.Blog.id == id)#.\
    if not db_blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Blog with id {id} not found')
    db_blog.delete(synchronize_session=False)
    db.commit()
    return {'detail':f'blog with id {id} deleted'}


@app.put('/blog/{id}', 
         status_code=status.HTTP_202_ACCEPTED,
         tags=['Blog']
         )
def update_blog(id: int, blog: schemas.Blog, db: Session = Depends(get_db)):
    db_blog = db.query(models.Blog).filter(models.Blog.id == id)#.\
    if not db_blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Blog with id {id} not found')
    db_blog.update(blog.model_dump())
    db.commit()
    return {'details': f'Blog with id {id} updated sucessfully'}


@app.get('/blog', response_model = List[schemas.ShowBlog],
          tags=['Blog'])
def get_blogs(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


@app.get('/blog/{id}', status_code=status.HTTP_200_OK,
         response_model=schemas.ShowBlog,
          tags=['Blog'])
def get_single_blog(id:int, response: Response,
                    db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Blog with id {id} not found')
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'detail':f'Blog with id {id} not found'}
    return blog

#-------------------User----------------------


@app.post("/user", 
          response_model=schemas.ShowUser,
          tags=['User'])
def create_user(user: schemas.User,
                db: Session = Depends(get_db)):
    
    new_user = models.User(name = user.name,
                           email = user.email,
                           password = Hash.encrypt(user.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get("/user/{id}", 
          response_model=schemas.ShowUser,
          tags=['User'])
def get_user(id: int,
             db: Session = Depends(get_db)):
    
    db_user = db.query(models.User).filter(models.User.id == id).first()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = f'User with id {id} not found')
    
    return db_user