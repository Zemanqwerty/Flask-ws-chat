from app import db
from ..models.Messages import Messages
from ..models.Chat import Chats


# Функция создания нового сообщения
def create(message_data):
    # получение чата для проверки, находится ли пользователь в нужном чате
    chat = db.session.query(Chats).filter(Chats.id==int(message_data['chat_id'])).first()
    # проверка наличия пользователя в чате
    if int(message_data['user_id']) == int(chat.user_id1) or int(message_data['user_id']) == int(chat.user_id2):
        # Создание записи о сообщении
        msg = Messages(chat_id=message_data['chat_id'], user_id=message_data['user_id'], message=message_data['message_text'])
        db.session.add(msg)
        db.session.commit()

        return f'message saved'
    else:
        return f'user {message_data.user_id} not in chat'


# Получение списка всех сообщений
def get_messages_list():
    messages = Messages.query.all()
    return messages


def get_messages_for_chat(chat_id: int):
    messages = db.session.query(Messages).filter(Messages.chat_id==chat_id)
    return messages


# Получение информации о конкретном сообщении
def get_current_message(message_id):
    message = db.session.query(Messages).filter(Messages.id==message_id).first()
    return message


# Обновление информации о конкретном сообщении
def update_message(message_data, message_id):
    msg = db.session.query(Messages).filter(Messages.id==message_id).first()
    
    # Переопределение информации о сообщении
    msg.chat_id = message_data.chat_id
    msg.user_id = message_data.user_id
    msg.message = message_data.message

    db.session.commit()
    return f'message updated'


# Удаление конкретного сообщения
def delete_message(message_id):
    message = Messages.query.filter_by(id=message_id).delete()
    db.session.commit()

    return f'message with id {message_id} deleted'