from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session

from .. import schemas, oauth2
from ..repository import blog
from ..database import get_db

router = APIRouter(
    prefix = "/blog",
    tags = ['Blogs']
)

@router.get('/', 
            response_model = List[schemas.ShowBlog])
def get_blogs(db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return blog.get_all(db)


@router.post("/", 
             status_code = status.HTTP_201_CREATED)
def create(blog_object: schemas.Blog, db : Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    # return {'title':blog.title,'body':blog.body}
    return blog.create(blog_object,current_user.id,db)


@router.delete("/{id}", 
               status_code = status.HTTP_204_NO_CONTENT)
def delete_blog(id: int, db : Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
   return blog.delete(id, db)


@router.put('/{id}', 
            status_code=status.HTTP_202_ACCEPTED)
def update_blog(id: int, blog_object: schemas.Blog, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return blog.update(id, blog_object, db)


@router.get('/{id}', status_code=status.HTTP_200_OK,
         response_model=schemas.ShowBlog)
def get_single_blog(id:int,
                    # response: Response,
                    db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return blog.show(id, db)

