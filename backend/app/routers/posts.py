




from fastapi import APIRouter, status, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db
from ..utils import Generate
from ..oauth2 import JWTToken
from ..queries import Query
from ..config import page_size
from typing import Optional, List

router = APIRouter(
    prefix="/post",
    tags=['Posts']
)




@router.post("/", status_code=status.HTTP_201_CREATED)
def create_post(post: schemas.PostIn, db: Session = Depends(get_db), current_user: int = Depends(JWTToken.get_current_user)):
    user = Query(db = db, model = models.User, id = current_user.id).get()
    if user.status != "Administrator" and post.iscomment == False:
        HTTPException(status_code=status.HTTP_401_UNAUTHORISED,
                    detail=f"You don't have permission to use this method")
    post_query = Query(db = db, model = models.Post)
    post.by_user_id = user.id
    post_obj = post_query.create(**post.dict())
    post_obj.by_user = user
    return post_obj
    
@router.get("/posts", status_code = status.HTTP_200_OK, response_model = List[schemas.PostOut])
def get_posts(offset: Optional[int] = 0, page: Optional[int] = 1, db: Session = Depends(get_db)):
    
    query = db.query(models.Post).filter(models.Post.iscomment == False).limit(page_size)
    if page > 1:
        query = query.offset( page * page_size )
    items = []
    for item in query.all():
        items.append(item)
    return items


@router.get("/{post_id}", status_code=status.HTTP_200_OK, response_model=schemas.FullPost)
def get_post(post_id: int, db: Session = Depends(get_db)):
    post_query = Query(db=db, model=models.Post, id=post_id)
    post_query.validate_existance()
    post = post_query.get()

    comments = db.query(models.Post).filter(
        models.Post.iscomment == True,
        models.Post.response_to_id == post.id
    ).all()

   

    response = {
        "post": post,
        "comments": comments
    }

    return response
