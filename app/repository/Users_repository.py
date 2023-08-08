from app import db
from ..models.User import Users


# Функция создания пользователя
def create(name, token, status, time_connected):
    user = Users(name=name, token=token, time_connected=time_connected, status=status)
    db.session.add(user)
    db.session.commit()

    return f'user {name} created'


# Функция получения списка пользователей
def get_users_list():
    users = Users.query.all()
    return users


# Функция получения конкретного пользователя
def get_current_user(user_id):
    user = db.session.query(Users).filter(Users.id==user_id).first()
    return user


# Функция обновления информации о конкретном пользователе
def update_user(user_data, user_id):
    user = db.session.query(Users).filter(Users.id==user_id).first()
    
    # Переопределение данных о пользователе
    user.name = user_data.name

    db.session.commit()
    return f'user {user_id} updated'


# Функция удаления конкретного пользователя
def delete_user(user_id):
    user = Users.query.filter_by(id=user_id).delete()
    db.session.commit()

    return f'user with uuid {user_id} deleted'