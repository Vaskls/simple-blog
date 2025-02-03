




from fastapi import APIRouter, status, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from .. import schemas
from ..utils import Generate


router = APIRouter(
    prefix="/cat",
    tags=['Cats']
)




@router.get("/", status_code=status.HTTP_200_OK, response_model=schemas.CatOut)
def get_cat_picture():
    cat_picture = Generate.random_cat()
    
    return {
        "url": cat_picture
    } 
