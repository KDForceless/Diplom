from database.models import User
from database import get_db
from datetime import datetime


# регистрация + проверка не занят ли юзер, mail и номер
def register_user_db(name: str, phone_number: str, email: str, password: str,
                     user_city: str= None):
    with next(get_db()) as db:
        checker = check_user(name, phone_number, email)
        if checker == True:
            new_user = User(name=name, phone_number=phone_number, email=email,
                            password=password, user_city=user_city,
                            reg_date=datetime.now())
            db.add(new_user)
            db.commit()
            return new_user.id
        else:
            return checker



def check_user(name=None, phone_number=None, email=None):
    with next(get_db()) as db:
        check_by_name = db.query(User).filter_by(name=name).first()
        check_by_phone = db.query(User).filter_by(phone_number=phone_number).first()
        check_by_email = db.query(User).filter_by(email=email).first()
        if check_by_name:
            return "Имя занято"
        elif check_by_phone:
            return "Номер занят"
        elif check_by_email:
            return "Почта занята"
        else:
            return True


#вход в аккаунт
def check_user_password_db(login, password):
    with next(get_db()) as db:
        check = db.query(User).filter_by(phone_number=login).first()
        check_user_email = db.query(User).filter_by(email=login).first()
        if check:
            if check.password == password:
                return check.id
            else:
                return False
        elif check_user_email:
            if check_user_email.password == password:
                return check_user_email.id
            else:
                return False
        elif not check and not check_user_email:
            return "Нет такого пользователя"


#получение данных о пользователе
def profile_info_db(user_id):
    with next(get_db()) as db:
        check = db.query(User).filter_by(id=user_id).first()
        if check:
            return check.id, check.name, check.phone_number, check.email, check.user_city
        return "Пользователь не найден"


#изменение данных пользователя(email, phone_num, user_name, user_city)
#password

def change_user_data_db(user_id, changeable_info, new_data):
    with next(get_db()) as db:
        check = db.query(User).filter_by(user_id=user_id).first()

        if check:
            if changeable_info == "email":
                check_info = check_user(email=new_data)
                if check_info == True:
                    check.email = new_data
            elif changeable_info == "phone_number":
                check_info = check_user(phone_number=new_data)
                if check_info == True:
                    check.phone_number = new_data
            elif changeable_info == "user_name":
                check_info = check_user(name=new_data)
                if check_info == True:
                    check.user_name = new_data
            elif changeable_info == "user_city":
                check.user_city = new_data
            elif changeable_info == "password":
                check.password = new_data
        db.commit()
        return "Информация успешно изменена"


#удаления юзера
def delete_user_db(user_id):
    with next(get_db()) as db:
        check = db.query(User).filter_by(user_id=user_id).first()
        if check:
            db.delete(check)
            return True
        db.commit()

