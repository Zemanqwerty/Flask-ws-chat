import json
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_socketio import SocketIO, join_room, leave_room, emit
from flask_session import Session
from ..pydantic_models.Messages import CreateMessage, UpdateMessage
from flask_pydantic import validate
from ..services import File_service
from flask_sqlalchemy import SQLAlchemy
from app import app


# Маршрут добавления файла
@app.route('/files/upload', methods=['POST'])
@validate()
def create_message():
    if 'file' not in request.files:
        return jsonify({'message': 'file is not selected'})
    
    file = request.files['file']

    if file.filename == '':
        return jsonify({'message': 'file is not selected'})
    
    if file and File_service.is_allowed_file(file.filename):
        # сохраняем запись
        return File_service.upload_file(file=file, message_data=json.loads(request.form.get('data')))
    else:
        return jsonify({'message': 'file type not allowed'})


# Маршрут получения списка всех файлов
@app.route('/files/all', methods=['GET'])
def get_all_files():
    return File_service.get_files_list()


# Маршрут получения информации о конкретном файле
@app.route('/files/<file_id>/info', methods=['GET'])
def get_current_file(file_id: int):
    return File_service.get_current_file(file_id=file_id)


# Маршрут обновления данных конкретного файла
@app.route('/files/<file_id>/update', methods=['PUT'])
@validate()
def update_file(file_id: int):
    if 'file' not in request.files:
        return jsonify({'message': 'file is not selected'})
    file = request.files['file']
    if file.filename == '':
        return jsonify({'message': 'file is not selected'})
    if file and File_service.allowed_file(file.filename):
        return File_service.update_file(file=file, message_data=json.loads(request.form.get('data')), file_id=file_id)
    else:
        return jsonify({'message': 'file type not allowed'})


# Маршрут удаления конкретного файла
@app.route('/files/<file_id>/delete', methods=['DELETE'])
@validate()
def delete_file(file_id: int):
    return File_service.delete_file(file_id=file_id)
