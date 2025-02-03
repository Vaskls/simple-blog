from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import database, schemas, models, oauth2
from ..utils import verify_password
from ..database import get_db
from ..oauth2 import JWTToken

router = APIRouter(tags=['Authentication'])

@router.post('/auth', response_model=schemas.Token)
def auth(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    
    user = db.query(models.User).filter(
        models.User.username == user_credentials.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

    if not verify_password(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    oauth = oauth2.JWTToken(subject={"user_id": user.id})
    token = oauth.create_token()
    return {"access_token": token, "token_type": "bearer"}

