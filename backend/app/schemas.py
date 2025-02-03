from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from datetime import datetime


class UserIn(BaseModel):
    username: str
    password: str

class PostIn(BaseModel):
    header: Optional[str]
    contents: str
    iscomment: bool
    by_user_id: Optional[int] = 0
    response_to_id: Optional[int] = None
    
class UserOut(BaseModel):
    id: int
    username: str
    status: str
    avatar: str
    joined: datetime
    total_posts: Optional[int] = 0
    total_reactions: Optional[int] = 0
    
    class Config:
        from_attributes = True
    
class UserUpdate(BaseModel):
    username: Optional[str] = ''
    avatar: Optional[str] = ''
    password: str
    newPassword: Optional[str] = ''
    
class PostOut(BaseModel):
    id: int
    ispinned: bool
    header: str
    contents: str
    iscomment: bool
    response_to_id: Optional[int] = None
    created: datetime
    by_user_id: int
    by_user: UserOut
    
    class Config:
        from_attributes = True

class FullPost(BaseModel):
    post: PostOut
    comments: Optional[List[PostOut]] = []



class Token(BaseModel):
    access_token: str
    token_type: str


class ReactionIn(BaseModel):
    post_id: int
    value: bool

class PostReactions(BaseModel):
    likes: int
    dislikes: int

class UserReaction(BaseModel):
    value: Optional[bool] = None

class TokenData(BaseModel):
    id: Optional[str] = None

class CatOut(BaseModel):
    url: str