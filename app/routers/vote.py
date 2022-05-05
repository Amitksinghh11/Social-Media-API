from hashlib import new
from pyexpat import model
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import schemas, database, models, oauth2

router = APIRouter(
    prefix="/vote",
    tags=["Vote"]
)

@router.post("/", status_code= status.HTTP_201_CREATED)
def vote(vote: schemas.Vote,db: Session = Depends(database.get_db),current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.PostModel).filter(models.PostModel.id == vote.post_id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "Post Does'nt Exists!")

    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()
    
    if vote.delete_vote == False:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail= f"User {current_user.id} Has Already Voted On Post {vote.post_id}!")
        new_vote = models.Vote(user_id=current_user.id,post_id = vote.post_id)
        db.add(new_vote)
        db.commit()
        return {"message": "Voted Succesfully!"}
    else:
        if not found_vote:
            raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail="No Vote Exist!")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message" : "Vote Deleted Succesfully"}
