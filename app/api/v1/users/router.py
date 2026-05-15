from uuid import UUID

from fastapi import APIRouter, Body, Depends, HTTPException, Query, Response, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
import logging

from app.api.v1.users import schemas, crud
from app.core.database import get_db

router = APIRouter(prefix="/users", tags=["Users"])
logger = logging.getLogger(__name__)


@router.post(
    "/",
    response_model=schemas.UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user",
    description="""
Registers a new user in the system. Fails if the email or username is already taken.

**Example using cURL:**
```bash
curl -X POST http://localhost:8000/users/ \
    -H "Content-Type: application/json" \
    -d '{"username":"jennma","email":"jennymartinez@gmail.com","first_name":"Jenny Paola","last_name":"Martínez","role":"user","active":true}'

```
""",
responses={ 
    400: {
        "description": "Email or Username already registered",
        "content": {
            "application/json": {
                "example": {"detail": "Email already registered"}
            }
        }
    }
}
)
async def create_user(
    user: schemas.UserCreate = Body(..., description="User payload"),
    db: AsyncSession = Depends(get_db),
):
    logger.info(f"Creating user with email {user.email}")
    db_user_email = await crud.get_user_by_email(db, email=user.email)
    if db_user_email:
        raise HTTPException(status_code=400, detail="Email already registered")
        
    db_user_username = await crud.get_user_by_username(db, username=user.username)
    if db_user_username:
        raise HTTPException(status_code=400, detail="Username already registered")
        
    return await crud.create_user(db=db, user=user)

@router.get(
    "/",
    response_model=List[schemas.UserResponse],
    summary="Read Users",
    description="""
    Retrieves a paginated list of users from the system. 

    **Example using cURL:**
    ```bash
    curl -X GET "http://localhost:8000/users/?skip=0&limit=100"
    
    ```

    """,
    responses={
        200: {
            "description": "Successful Response - Returns a list of users."
        }
}
)
async def read_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: AsyncSession = Depends(get_db),
):
    users = await crud.get_users(db, skip=skip, limit=limit)
    return users

@router.get(
    "/{user_id}",
    response_model=schemas.UserResponse,
    summary="Get user by ID",
    description="""
        Retrieves a specific user from the database using their unique identifier.

        **Example using cURL:**
        ```bash
        curl -X GET "http://localhost:8000/users/TU-UUID-AQUI"
       
        ```

        """,
    responses={
        404: {"description": "User not found", "content": {"application/json": {"example": {"detail": "User not found"}}}}
    }
)
async def read_user(user_id: UUID, db: AsyncSession = Depends(get_db)):
    db_user = await crud.get_user_by_id(db, user_id=str(user_id))
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.put(
    "/{user_id}",
    response_model=schemas.UserResponse,
    summary="Update a user",
    description="""
        Updates an existing user's information. Fails if the user is not found, or if the new email or username is already in use by another user.

        **Example using cURL:**
        ```bash
        curl -X PUT http://localhost:8000/users/TU-UUID-AQUI \
            -H "Content-Type: application/json" \
            -d '{"first_name":"Luis Esteban","role":"admin"}'
       
        ```

        """,
    responses={
    200: {
        "description": "User successfully updated"
    },
    400: {
        "description": "Email or Username already registered by another user",
        "content": {
            "application/json": {
                "example": {"detail": "Email already registered"}
            }
        }
    },
    404: {
        "description": "User not found in the database",
        "content": {
            "application/json": {
                "example": {"detail": "User not found"}
            }
        }
    }
}
)
async def update_user(
    user_id: UUID,
    user_update: schemas.UserUpdate = Body(..., description="User update payload"),
    db: AsyncSession = Depends(get_db),
):
    logger.info(f"Updating user {user_id}")
    if user_update.email:
        existing = await crud.get_user_by_email(db, email=user_update.email)
        if existing and str(existing.id) != str(user_id):
            raise HTTPException(status_code=400, detail="Email already registered")

    if user_update.username:
        existing = await crud.get_user_by_username(db, username=user_update.username)
        if existing and str(existing.id) != str(user_id):
            raise HTTPException(status_code=400, detail="Username already registered")

    db_user = await crud.update_user(db, user_id=str(user_id), user_update=user_update)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.delete(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=schemas.MessageResponse, 
    summary="Delete a user",
    description="""
        Deletes a user from the system permanently. Fails if the user is not found.

        **Example using cURL:**
        ```bash
        curl -X DELETE "http://localhost:8000/users/TU-UUID-AQUI"
        
        ```

        """,
    responses={
        200: {
            "description": "User successfully deleted"
        },
        404: {
            "description": "User not found in the database",
            "content": {
                "application/json": {
                    "example": {"detail": "User not found"}
                }
            }
        }
    }
)
async def delete_user(user_id: UUID, db: AsyncSession = Depends(get_db)):
    logger.info(f"Deleting user {user_id}")
    success = await crud.delete_user(db, user_id=str(user_id))
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"detail": "User successfully deleted"}
