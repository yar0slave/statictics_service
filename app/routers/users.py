from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.orm import Session

from app.models.database import get_db
from app.schemas.user import User, UserCreate, UserUpdate, UserWithDevices
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=List[User])
def read_users(
        skip: int = Query(0, ge=0),
        limit: int = Query(100, ge=1, le=100),
        db: Session = Depends(get_db)
):

    users = UserService.get_users(db, skip=skip, limit=limit)
    return users


@router.post("/", response_model=User, status_code=201)
def create_user(
        user: UserCreate,
        db: Session = Depends(get_db)
):
    db_user = UserService.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    db_user = UserService.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already taken")

    return UserService.create_user(db=db, user=user)


@router.get("/{user_id}", response_model=UserWithDevices)
def read_user(
        user_id: int = Path(...),
        db: Session = Depends(get_db)
):
    db_user = UserService.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.put("/{user_id}", response_model=User)
def update_user(
        user_id: int = Path(...),
        user_update: UserUpdate = None,
        db: Session = Depends(get_db)
):
    db_user = UserService.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    if user_update.email and user_update.email != db_user.email:
        existing_user = UserService.get_user_by_email(db, email=user_update.email)
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")

    if user_update.username and user_update.username != db_user.username:
        existing_user = UserService.get_user_by_username(db, username=user_update.username)
        if existing_user:
            raise HTTPException(status_code=400, detail="Username already taken")

    updated_user = UserService.update_user(db=db, user_id=user_id, user_update=user_update)
    return updated_user


@router.delete("/{user_id}", status_code=204)
def delete_user(
        user_id: int = Path(...),
        db: Session = Depends(get_db)
):
    db_user = UserService.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    deleted = UserService.delete_user(db=db, user_id=user_id)
    if not deleted:
        raise HTTPException(status_code=500, detail="Failed to delete user")