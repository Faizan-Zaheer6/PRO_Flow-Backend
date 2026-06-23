from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.repositories.user import user_repo
from app.core.security import verify_password, create_access_token

class AuthService:
    async def authenticate_user(self, session: AsyncSession, form_data: OAuth2PasswordRequestForm):
        user = await user_repo.get_by_email(session, email=form_data.username)
        if not user:
            raise HTTPException(status_code=400, detail="Incorrect email or password")
        if not verify_password(form_data.password, user.hashed_password):
            raise HTTPException(status_code=400, detail="Incorrect email or password")
        if not user.is_active:
            raise HTTPException(status_code=400, detail="Inactive user")
            
        access_token = create_access_token(subject=user.id, role=user.role)
        return {"access_token": access_token, "token_type": "bearer"}

auth_service = AuthService()
