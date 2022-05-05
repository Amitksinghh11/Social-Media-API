from xml.parsers.expat import model
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from typing import List, Optional
from sqlalchemy import func
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix= "/posts",
    tags= ["Posts"]
)

@router.get("/", response_model= List[schemas.Post])
def get_my_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    posts = db.query(models.PostModel).filter(models.PostModel.owner_id == current_user.id).all()
    return posts


# limit -> Query Parameter
# to get a space in query parameter -> %20
@router.get("/feeds", response_model= List[schemas.PostOut])
def get_feeds(db: Session = Depends(get_db), limit:int = 10, skip:int = 0, search:Optional[str] = ""):
    #cursor.execute("""SELECT * FROM posts """)
    #posts = cursor.fetchall()

    results = db.query(models.PostModel, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.PostModel.id, isouter= True).group_by(models.PostModel.id).filter(models.PostModel.title.contains(search)).limit(limit).offset(skip).all()

    return results


@router.post("/", status_code= status.HTTP_201_CREATED, response_model= schemas.Post)
def create_posts(post:schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""INSERT INTO posts (title, content) VALUES (%s, %s) RETURNING * """, (post.title, post.content))
    # new_post = cursor.fetchone()
    # conn.commit()

    new_post = models.PostModel(owner_id = current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/{id}", response_model= schemas.PostOut) 
def get_a_post(id:int,db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id)))
    # post = cursor.fetchone()

    post = db.query(models.PostModel, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.PostModel.id, isouter= True).group_by(models.PostModel.id).filter(models.PostModel.id == id).first()
    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"Id: {id} Not Found!!")
    return post

@router.delete("/{id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """, (str(id)))
    # deleted_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.PostModel).filter(models.PostModel.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"Id: {id} Not Found")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail="Unauthorized Action Request")
    
    post_query.delete(synchronize_session= False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model= schemas.Post)
def update_post(id:int, post:schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE posts SET title = %s, content = %s WHERE id = %s RETURNING * """, (post.title, post.content, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.PostModel).filter(models.PostModel.id == id)
    found_post = post_query.first()
    
    if found_post == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"Id: {id} Not Found")
    
    if found_post.owner_id != current_user.id:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail="Unauthorized Action Request")
    
    post_query.update(post.dict(), synchronize_session= False)
    db.commit()
    return post_query.first()