import json
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, join_room, leave_room, emit
from flask_session import Session
from flask_pydantic import validate

from app import app, logger, sock, socket_clients_list
from ..pydantic_models.Messages import CreateMessage, UpdateMessage
from ..services import Message_service, File_service, User_service


@sock.route('/message')
def send_message(ws):
    # Получение списка пользователей в группе
    room = socket_clients_list[session.get('room')]
    # Добавление пользователя в группу
    room.append(ws)
    while ws.connected:
        raw_message = ws.receive()
        print(raw_message)
        json_message = json.loads(raw_message)

        json_message.update({
            'user_id': int(session.get('user_id')),
            'chat_id': int(session.get('room'))    
        })

        # Если получено текстовое сообщение
        if 'message_text' in json_message and json_message['message_text']:
            # Запись сообщения в БД
            Message_service.create_message(message_data=json_message)
            # Броадкаст рассылка сообщения в группе пользователей
            for client in room:
                client.send(json.dumps(json_message))

        # Если получен файл
        elif 'file' in json_message and json_message['file'] and json_message['file_name']:
            # Запись файла в БД
            file_path = File_service.convert_upload_file(data=json_message)
            # Броадкаст рассылка файла в группе пользователей
            for client in room:
                client.send(json.dumps({
                    'user_id': session.get('user_id'),
                    'chat_id': json_message['chat_id'],
                    'file_src': file_path
                }))
