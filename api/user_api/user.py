from fastapi import APIRouter
from database.userservice import register_user_db, check_user_password_db, profile_info_db, change_user_data_db, delete_user_db
from pydantic import BaseModel
from typing import Optional


user_router = APIRouter(prefix='/user', tags=['Пользователи'])

class UserValidator(BaseModel):
    name: str
    phone_number: str
    email: str
    password: str
    user_city: Optional[str] = None



@user_router.post('/registraion')
async def register_user(validator: UserValidator):
    user_dict = validator.dict()
    user = register_user_db(**user_dict)
    return {'status': 1, 'message': 'Успешная регистрация'} if user else {'status': 0, 'message': 'Ошибка в регистрации'}


@user_router.post('/login')
async def login_user(login:str, password: str):
    user = check_user_password_db(login, password)
    return {'status': 1, 'message': user} if user else {'status': 0, 'message': user}

@user_router.post('/get_user')
async def get_user(user_id: int):
    user = profile_info_db(user_id)
    return user


@user_router.put('/change_profile')
async def change_user_profile(user_id: int, change_info: str, new_data: str):
    user = change_user_data_db(user_id, change_info, new_data)
    return user


@user_router.delete('/delete_user')
async def delete_user(user_id: int):
    user = delete_user_db(user_id)
    return {'status': 1, 'message': "Пользователь успешно удален"} if user else {'status': 0, 'message': "Что то пошло не так"}