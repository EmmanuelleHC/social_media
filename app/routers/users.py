from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from .. import models, database, auth

router = APIRouter(prefix="/users", tags=["Users"])
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/login_form", response_class=HTMLResponse)
def login_form(request: Request, username: str = Form(...), password: str = Form(...), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user or not auth.verify_password(password, user.password):
        return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid username or password"})
    
    response = RedirectResponse("/users/dashboard", status_code=303)
    response.set_cookie("username", user.username)
    return response


@router.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@router.post("/register_form", response_class=HTMLResponse)
def register_form(request: Request, username: str = Form(...), email: str = Form(...), password: str = Form(...), db: Session = Depends(database.get_db)):
    existing_user = db.query(models.User).filter(models.User.username == username).first()
    if existing_user:
        return templates.TemplateResponse("register.html", {"request": request, "error": "Username already exists"})
    
    hashed_pw = auth.get_password_hash(password)
    new_user = models.User(username=username, email=email, password=hashed_pw)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    response = RedirectResponse("/users/", status_code=303)
    return response


@router.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request, username: str = None, db: Session = Depends(database.get_db)):
    username_cookie = request.cookies.get("username")
    if not username_cookie:
        return RedirectResponse("/users/", status_code=303)
    
    posts = db.query(models.Post).order_by(models.Post.created_at.desc()).all()
    return templates.TemplateResponse("dashboard.html", {"request": request, "username": username_cookie, "posts": posts})
