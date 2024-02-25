from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session

from .. import schemas, models
from ..database import get_db

router = APIRouter()

@router.get('/blog', response_model = List[schemas.ShowBlog],
          tags=['Blog'])
def get_blogs(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


@router.post("/blog", 
          status_code = status.HTTP_201_CREATED,
          tags=['Blog'])
def create(blog: schemas.Blog, db : Session = Depends(get_db)):
    # return {'title':blog.title,'body':blog.body}
    new_blog = models.Blog(title = blog.title,
                           body = blog.body,
                           user_id = 1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@router.delete("/blog/{id}", 
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


@router.put('/blog/{id}', 
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


@router.get('/blog/{id}', status_code=status.HTTP_200_OK,
         response_model=schemas.ShowBlog,
          tags=['Blog'])
def get_single_blog(id:int,
                    # response: Response,
                    db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Blog with id {id} not found')
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'detail':f'Blog with id {id} not found'}
    return blog

