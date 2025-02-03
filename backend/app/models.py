from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, text
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from .database import engine, Base
from .utils import Generate


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String(255), nullable=False, unique = True) # added unique
    # salt = Column(String(16), nullable=False)
    password = Column(String, nullable=False)
    status = Column(String, nullable=False, default = "User") # added default
    avatar = Column(String, nullable=True) # added nullable
    joined = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    posts = relationship("Post", back_populates="by_user") # fixed backref
    reactions = relationship("Reaction", back_populates="by_user")

    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password
        self.avatar = Generate.random_cat()

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, status={self.status})>"



class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    ispinned = Column(Boolean, nullable=False, default=False)

    header = Column(String(255), nullable=False, default="UNASSIGNED")
    contents = Column(String(4096), nullable=True)

    iscomment = Column(Boolean, default=False, nullable=False)

    created = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    response_to_id = Column(Integer, ForeignKey('posts.id'), nullable=True)
    response_to = relationship("Post", remote_side=[id], backref="replies")

    by_user_id = Column(Integer, ForeignKey("users.id"))
    by_user = relationship("User", back_populates="posts")  
    
    reactions = relationship("Reaction", back_populates="post") 


    def __repr__(self):
        return f"<Post(id={self.id}, header='{self.header}', iscomment={self.iscomment}, response_to_id={self.response_to_id})>"


class Reaction(Base):
    __tablename__ = "reactions"

    id = Column(Integer, primary_key=True, nullable=False)

    by_user_id = Column(Integer, ForeignKey("users.id"))
    post_id = Column(Integer, ForeignKey("posts.id"))
    value = Column(Boolean, nullable=False)  # True - like, False - dislike

    by_user = relationship("User", back_populates="reactions")
    post = relationship("Post", back_populates="reactions") 

    def __init__(self, value, post_id, by_user_id):
        self.value = value
        self.post_id = post_id
        self.by_user_id = by_user_id



# Create all tables if they don't exist
Base.metadata.create_all(bind=engine)