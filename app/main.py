from fastapi import FastAPI, Request, Depends, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
import os

from . import models, database, auth
from .routers import users, posts


models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Social Media App - FastAPI + MySQL + HTML")

os.makedirs("app/static", exist_ok=True)
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")


app.include_router(users.router)
app.include_router(posts.router)


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    """Show login page"""
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/register", response_class=HTMLResponse)
def show_register(request: Request):
    """Show register page"""
    return templates.TemplateResponse("register.html", {"request": request})

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request, db: Session = Depends(database.get_db)):
    """Show dashboard with posts"""
    username_cookie = request.cookies.get("username")
    if not username_cookie:
        return RedirectResponse("/", status_code=303)
    
    user = db.query(models.User).filter(models.User.username == username_cookie).first()
    if not user:
        return RedirectResponse("/", status_code=303)
    
    posts = db.query(models.Post).order_by(models.Post.created_at.desc()).all()
    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request, "username": user.username, "posts": posts}
    )


@app.post("/login_form", response_class=HTMLResponse)
def login_form(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(database.get_db)
):
    """Handle login form submission"""
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user or not auth.verify_password(password, user.password):
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error": "Invalid username or password"}
        )
    
    response = RedirectResponse("/dashboard", status_code=303)
    response.set_cookie(
        key="username",
        value=user.username,
        httponly=True,
        samesite="lax"
    )
    return response

@app.post("/register_form", response_class=HTMLResponse)
def register_form(
    request: Request,
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(database.get_db)
):
    """Handle registration form submission"""
    existing_user = db.query(models.User).filter(models.User.username == username).first()
    if existing_user:
        return templates.TemplateResponse(
            "register.html",
            {"request": request, "error": "Username already registered"}
        )
    
    hashed_pw = auth.get_password_hash(password)
    new_user = models.User(username=username, email=email, password=hashed_pw)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return RedirectResponse(url="/", status_code=303)
