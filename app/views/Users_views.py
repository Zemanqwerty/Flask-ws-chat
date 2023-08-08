from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_socketio import SocketIO, join_room, leave_room, emit
from flask_session import Session
from ..pydantic_models.Users import CreateUser, UpdateUser
from flask_pydantic import validate
from ..services import User_service
from flask_sqlalchemy import SQLAlchemy
from app import app


# Маршрут для создания пользователя
@app.route('/users/create', methods=['POST'])
@validate()
def create_user(body: CreateUser):
    return User_service.create_user(user_data=body)

# Маршрут для получения списка всех пользователей
@app.route('/users/all', methods=['GET'])
def get_all_users():
    return User_service.get_users_list()

# Маршрут для получения информации о конкретном пользователе
@app.route('/users/<user_id>/info', methods=['GET'])
def get_current_user(user_id: int):
    return jsonify(User_service.get_current_user(user_id=user_id))

# Маршрут для обновления информации о пользователе
@app.route('/users/<user_id>/update', methods=['PUT'])
@validate()
def update_user(user_id: int, body: UpdateUser):
    return User_service.update_user(user_data=body, user_id=user_id)

# Маршрут для удаления пользователя
@app.route('/users/<user_id>/delete', methods=['DELETE'])
@validate()
def delete_user(user_id: int):
    return User_service.delete_user(user_id=user_id)