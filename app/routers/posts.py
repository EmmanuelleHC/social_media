from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from .. import models, database

router = APIRouter(prefix="/posts", tags=["Posts"])

@router.post("/create", response_class=RedirectResponse)
def create_post(request: Request, title: str = Form(...), content: str = Form(...), db: Session = Depends(database.get_db)):
    username = request.cookies.get("username")
    if not username:
        return RedirectResponse("/users/", status_code=303)
    
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        return RedirectResponse("/users/", status_code=303)
    
    new_post = models.Post(title=title, content=content, author=user)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return RedirectResponse("/users/dashboard", status_code=303)
