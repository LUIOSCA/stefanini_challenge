from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.api.v1.users import models, schemas
import uuid

async def get_user_by_id(db: AsyncSession, user_id: str):
    """
    Obtiene un usuario único mediante su ID (UUID)

    """
    try:
        if isinstance(user_id, str):
            user_id_obj = uuid.UUID(user_id)
        else:
            user_id_obj = user_id
    except ValueError:
        return None
    result = await db.execute(select(models.User).filter(models.User.id == user_id_obj))
    return result.scalars().first()

async def get_user_by_email(db: AsyncSession, email: str):
    """
    Busca un usuario por su dirección de correo electrónico..

    """
    result = await db.execute(select(models.User).filter(models.User.email == email))
    return result.scalars().first()

async def get_user_by_username(db: AsyncSession, username: str):
    """
    Busca un usuario por su nombre de usuario único..
    """
    result = await db.execute(select(models.User).filter(models.User.username == username))
    return result.scalars().first()

async def get_users(db: AsyncSession, skip: int = 0, limit: int = 100):
    """
    Retorna una lista paginada de usuarios.
    """
    result = await db.execute(select(models.User).offset(skip).limit(limit))
    return result.scalars().all()

async def create_user(db: AsyncSession, user: schemas.UserCreate):
    """
    Crea un nuevo registro de usuario.
    Genera un UUID único antes de la inserción.
    """
    db_user = models.User(
        id=uuid.uuid4(),
        username=user.username,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        role=user.role,
        active=user.active
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def update_user(db: AsyncSession, user_id: str, user_update: schemas.UserUpdate):
    """
    Actualiza parcialmente un usuario existente.
    Usa 'exclude_unset' para modificar solo los campos enviados en el payload.
    """
    db_user = await get_user_by_id(db, user_id)
    if not db_user:
        return None
    
    update_data = user_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_user, key, value)
        
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def delete_user(db: AsyncSession, user_id: str):
    """
    Elimina permanentemente un usuario de la base de datos.
    """
    db_user = await get_user_by_id(db, user_id)
    if db_user:
        await db.delete(db_user)
        await db.commit()
        return True
    return False
