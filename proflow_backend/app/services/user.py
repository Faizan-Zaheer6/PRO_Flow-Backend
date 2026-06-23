from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from app.repositories.user import user_repo
from app.schemas.user import UserCreate
from app.core.security import get_password_hash

class UserService:
    async def create_user(self, session: AsyncSession, user_in: UserCreate):
        user = await user_repo.get_by_email(session, email=user_in.email)
        if user:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        user_dict = user_in.model_dump(exclude={"password"})
        user_dict["hashed_password"] = get_password_hash(user_in.password)
        
        return await user_repo.create(session, obj_in=user_dict)

user_service = UserService()
