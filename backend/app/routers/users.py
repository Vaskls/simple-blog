




from fastapi import APIRouter, status, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db
from ..utils import Generate, verify_password
from ..oauth2 import JWTToken
from ..queries import Query


router = APIRouter(
    prefix="/user",
    tags=['User']
)




@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserIn, db: Session = Depends(get_db)):
    
    is_exists = db.query(models.User).filter(models.User.username == user.username).first()
    print(is_exists == None)
    if is_exists != None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"User with username '{user.username}' already exist!") 

    # user.salt = Generate.
    user.password = Generate.hashed_password(user.password)
    user_query = Query(db = db, model = models.User)
    user_query.create(**user.dict())
    return {"status": "ok"}


@router.delete("/{user_id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db), current_user: int = Depends(JWTToken.get_current_user)): 
    
    
    if current_user.id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")
    
    
    user_query = Query(db = db, model = models.User, id = user_id)
    user_query.delete()

    return Response(status_code=status.HTTP_204_NO_CONTENT)



@router.get("/username", status_code = status.HTTP_200_OK)
def check_username(username: str, db: Session = Depends(get_db)):
    user_obj = db.query(models.User).filter(models.User.username == username).first()
    username_exists = user_obj is not None

    return {
        "exists": username_exists
    }




@router.get("/me", status_code = status.HTTP_200_OK, response_model = schemas.UserOut)
def get_user(db: Session = Depends(get_db), current_user: int = Depends(JWTToken.get_current_user)):
    print(current_user)

    user_query = Query(db = db, model = models.User, id = current_user.id)
    user_query.validate_existance()
    user_object = user_query.get()
    user_object.total_posts = len(user_object.posts)
    user_object.total_reactions = len(user_object.reactions)
    return user_object



@router.get("/{user_id}", status_code = status.HTTP_200_OK, response_model = schemas.UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user_query = Query(db = db, model = models.User, id = user_id)
    user_query.validate_existance()
    user_object = user_query.get()
    
    return user_object

@router.put("/", status_code = status.HTTP_200_OK)
def update_user(schema: schemas.UserUpdate, db: Session = Depends(get_db), current_user: int = Depends(JWTToken.get_current_user)):
    print("USER", current_user, "UPDATE")
    if not verify_password(schema.password, current_user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    print(schema.dict())
    print("Password ok")
    if schema.avatar.startswith("https://"):
        print("Updating password")
        current_user.avatar = schema.avatar
    
    if schema.username != '':
        username_exists = db.query(models.User).filter(
            models.User.username == schema.username
        ).first()
        if username_exists != None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Username already exists")
        print("Updating username")
        current_user.username = schema.username

    if schema.newPassword != '':
        print("Updating password")
        current_user.password = Generate.hashed_password(schema.password)
    db.commit()
    
    return {
        "status": "ok"
    }