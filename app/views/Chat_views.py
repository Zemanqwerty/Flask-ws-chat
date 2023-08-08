from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, join_room, leave_room, emit
from app import app, socket_clients_list
from flask_pydantic import validate
from ..services import Chat_service
from ..pydantic_models.Chats import CreateChat, UpdateChat


# Маршрут отображения главной страницы
@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


# Маршрут определения нового пользователя и комнаты
@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if request.method == 'POST':
        
        user_id = request.form['username']
        room = request.form['room']
        session['user_id'] = user_id
        session['room'] = room

        room_is_created = socket_clients_list.get(room)

        if room_is_created is None:
            print('creating room...')
            socket_clients_list[room] = []
        return render_template('chat.html', session=session)
    elif session.get('username'):
        return render_template('chat.html', session=session)

    return redirect(url_for('index'))


# Маршрут создания нового чата
@app.route('/chat/create', methods=['POST'])
@validate()
def create_chat(body: CreateChat):
    return Chat_service.create_chat(chat_data=body)


# Маршрут получения списка всех чатов
@app.route('/chat/all', methods=['GET'])
def get_all_chats():
    return Chat_service.get_chats_list()


# Маршрут получения информации о конкретном чате
@app.route('/chat/<chat_id>/info', methods=['GET'])
def get_current_chat(chat_id: int):
    return Chat_service.get_current_chat(chat_id=chat_id)


# Маршрут обновления информации о конкретном чате
@app.route('/chat/<chat_id>/update', methods=['PUT'])
@validate()
def update_chat(chat_id: int, body: UpdateChat):
    return Chat_service.update_chat(chat_data=body, chat_id=chat_id)


# Маршрут удаления конкретного чата
@app.route('/chat/<chat_id>/delete', methods=['DELETE'])
@validate()
def delete_chat(chat_id: int):
    return Chat_service.delete_chat(chat_id=chat_id)
