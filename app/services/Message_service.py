from ..repository import Messages_repository, Users_repository, Files_repository
from flask import jsonify
from app import ALLOWED_EXTENSIONS, UPLOAD_FOLDER
import os
import app
from werkzeug.utils import secure_filename


# Функция создания нового сообщения
def create_message(message_data):
    try:
        return jsonify({'message': f'{Messages_repository.create(message_data=message_data)}'})
    except Exception as e:
        print(f'error message: {e}')
        return jsonify({'message': 'error'})


def get_messages_for_chat(chat_id: int):
    try:
        messages_list = Messages_repository.get_messages_for_chat(chat_id=chat_id)

        messages = []

        # Перебираются все сообщения, полученные в переменную messages_list
        for message in messages_list:
            messages.append(
                {   
                    'id': message.uuid,
                    'chat_id': message.chat_id,
                    'user_id': message.user_id,
                    'message': message.message
                }
            )

        return jsonify(messages)
    except Exception as e:
        print(e)
        return jsonify({'message': 'error'})


# Функция получения списка сообщений
def get_messages_list():
    try:
        messages_list = Messages_repository.get_messages_list()

        messages = []

        # Перебираются все сообщения, полученные в переменную messages_list
        for message in messages_list:
            messages.append(
                {   
                    'id': message.uuid,
                    'chat_id': message.chat_id,
                    'user_id': message.user_id,
                    'message': message.message
                }
            )

        return jsonify(messages)
    except Exception as e:
        print(e)
        return jsonify({'message': 'error'})


# Функция получения данных о конкретном сообщении
def get_current_message(message_id):
    try:
        message = Messages_repository.get_current_message(message_id=message_id)

        # Функция возвращает лишь определённые поля
        return jsonify({
            "id": message.uuid,
            "chat_id": message.chat_id,
            "user_id": message.user_id,
            'message': message.message
        })
    except Exception as e:
        print(e)
        return jsonify({'message': 'error'})


# Функция обновления данных конкретного сообщения
def update_message(message_data, message_id):
    try:
        return Messages_repository.update_message(message_data=message_data, message_id=message_id)
    except Exception as e:
        print(e)
        return jsonify({'message': 'error'})


# Функция удаления конкретного сообщения
def delete_message(message_id):
    try:
        return Messages_repository.delete_message(message_id=message_id)
    except Exception as e:
        print(e)
        return jsonify({'message': 'error'})