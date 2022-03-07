import uvicorn
import hashlib
import time
import jwt

from fastapi import FastAPI, Request, Response, Body, Depends, status, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from sqlalchemy.orm import Session
from database import SessionLocal
from app import crud, schemas, config


app = FastAPI(title="2022 Exam Monitoring System")
templates = Jinja2Templates(directory="templates")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    claims = jwt.decode(token, config.JWT_SECRET_KEY, algorithms=["HS256"])
    user_id = claims.get("id")
    user = crud.get_user(db=db, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_active_user(
    current_user: schemas.BaseUser = Depends(get_current_user),
):
    if current_user.is_active is False:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.get("/users/me")
async def read_users_me(
    current_user: schemas.BaseUser = Depends(get_current_active_user),
):
    return current_user


@app.post("/token")
async def login(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = crud.get_user_by_email(db, form_data.username)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    hashed_password = hashlib.md5(form_data.password.encode()).hexdigest()
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token_expires = time.time() + 3600 * 24 * 30
    access_token = jwt.encode(
        {
            "id": user.id,
            "email": user.email,
            "iat": time.time(),
            "exp": access_token_expires,
        },
        config.JWT_SECRET_KEY,
        algorithm="HS256",
    )
    token_type = "Bearer"
    response.set_cookie(key="access_token", value=access_token)
    response.set_cookie(key="token_type", value=token_type)
    return {"access_token": access_token, "token_type": token_type}


@app.post("/user/update/{user_id}")
async def update_user(
    user_id: int,
    body=Body(...),
    current_user: schemas.BaseUser = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    if current_user.role_id not in [1, 2] and user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="No permission"
        )
    user = crud.get_user(db, user_id=user_id)
    user.is_cheater = body.get("is_cheater", user.is_cheater)
    user.image = body.get("base64", user.image)
    db.commit()
    return crud.get_user(db, user_id=user_id)


@app.post("/user/create")
async def create_user(
    body=Body(...),
    current_user: schemas.BaseUser = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    print(body)
    if current_user.role_id not in [1, 2]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="No permission"
        )
    email = body.get("email")
    password = body.get("password")
    hashed_password = hashlib.md5(password.encode()).hexdigest()
    user = crud.create_user(db, email, hashed_password, 3)
    return user


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    access_token = request.cookies.get("access_token")
    token_type = request.cookies.get("token_type")
    if access_token and token_type:
        request.headers.__dict__["_list"].append(
            (
                "authorization".encode(),
                f"{token_type} {access_token}".encode(),
            )
        )
    response = await call_next(request)
    return response


@app.get("/", response_class=HTMLResponse)
async def login(request: Request):
    try:
        jwt.decode(
            request.headers.get("authorization"),
            config.JWT_SECRET_KEY,
            algorithms=["HS256"],
        )
        return RedirectResponse("/admin")
    except Exception:
        pass
    finally:
        return templates.TemplateResponse("login.html", {"request": request})


@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard_page(
    request: Request,
    current_user: schemas.User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    if current_user.role_id not in [1, 2]:
        students = [crud.get_user(db, user_id=current_user.id)]
    else:
        students = crud.get_students(db)
    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request, "current_user": current_user, "students": students},
    )


@app.get("/create", response_class=HTMLResponse)
async def create(
    request: Request,
    current_user: schemas.User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    if current_user.role_id not in [1, 2]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="No permission"
        )
    return templates.TemplateResponse(
        "create.html",
        {"request": request, "current_user": current_user},
    )


@app.get("/edit", response_class=HTMLResponse)
async def dashboard_page(
    request: Request,
    student_id: int,
    current_user: schemas.User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    student: schemas.User = crud.get_user(db, student_id)
    return templates.TemplateResponse(
        "edit.html",
        {"request": request, "current_user": current_user, "student": student},
    )


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, workers=2, debug=True)
