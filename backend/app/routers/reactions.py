




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
    prefix="/reaction",
    tags=['Posts']
)



@router.post("/", status_code=status.HTTP_201_CREATED)
def toggle_reaction(reaction: schemas.ReactionIn, db: Session = Depends(get_db), current_user: int = Depends(JWTToken.get_current_user)):
    post = Query(db = db, model = models.Post, id = reaction.post_id)
    post.validate_existance()

    print("POST EXISTS")
    reaction_query = db.query(models.Reaction).filter(
        models.Reaction.by_user_id == current_user.id,
        models.Reaction.post_id == post.get().id
    )
    print("query created")
    reaction_obj = reaction_query.first()
    if not reaction_obj:
        reaction_obj = models.Reaction(
            value = reaction.value,
            post_id = post.id,
            by_user_id = current_user.id
        )
        db.add(reaction_obj)
        db.commit()
        db.refresh(reaction_obj)
        return reaction_obj

    if reaction_obj.value == reaction.value: # undo reaction
        reaction_query.delete()
        db.commit()
        return {
            "status": "reaction deleted"
        }
    else: # change value
        reaction_obj.value = reaction.value
        db.commit()
        return {
            "status": "value changed"
        }

@router.get("/{post_id}/my", status_code=status.HTTP_200_OK, response_model=schemas.UserReaction)
def get_reactions(post_id: int, db: Session = Depends(get_db), current_user: int = Depends(JWTToken.get_current_user)):
    post = Query(db = db, model = models.Post, id = post_id)
    post.validate_existance()

    reaction = db.query(models.Reaction).filter(
        models.Reaction.post_id == post.id,
        models.Reaction.by_user_id == current_user.id
    ).first()
    value = None
    if reaction:
        value = reaction.value
    return {
        "value": value
    }


@router.get("/{post_id}", status_code=status.HTTP_200_OK, response_model = schemas.PostReactions)
def get_reactions(post_id: int, db: Session = Depends(get_db)):
    post = Query(db = db, model = models.Post, id = post_id)
    post.validate_existance()

    reactions = db.query(models.Reaction).filter(
        models.Reaction.post_id == post.id,
    ).all()
    likes, dislikes = 0, 0
    for reaction in reactions:
        if reaction.value == True: likes += 1  
        else: dislikes += 1
    return {
        "likes": likes,
        "dislikes": dislikes
    }
