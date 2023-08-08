import json
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_socketio import SocketIO, join_room, leave_room, emit
from flask_session import Session
from ..pydantic_models.Messages import CreateMessage, UpdateMessage
from flask_pydantic import validate
from ..services import Message_service
from flask_sqlalchemy import SQLAlchemy
from app import app


# маршрут получения списка всех сообщений
@app.route('/messages/all', methods=['GET'])
def get_all_messages():
    return Message_service.get_messages_list()


# Маршрут получения конкретного сообщения
@app.route('/messages/<message_id>/info', methods=['GET'])
def get_current_message(message_id: int):
    return Message_service.get_current_message(message_id=message_id)


# Маршрут обновления конкретного сообщения
@app.route('/messages/<message_id>/update', methods=['PUT'])
@validate()
def update_message(message_id: int, body: UpdateMessage):
    return Message_service.update_message(message_data=body, message_id=message_id)


# Маршрут удаления конкретного сообщения
@app.route('/messages/<message_id>/delete', methods=['DELETE'])
@validate()
def delete_message(message_id: int):
    return Message_service.delete_message(message_id=message_id)


@app.route('/messages/<chat_id>/all', methods=["GET"])
@validate()
def get_messages_for_chat(chat_id: int):
    return Message_service.get_messages_for_chat(chat_id=chat_id)