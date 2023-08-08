from ..repository import Users_repository, Files_repository
from flask import jsonify, session
from app import ALLOWED_EXTENSIONS, UPLOAD_FOLDER, logger
import os
import app
from werkzeug.utils import secure_filename
import PIL.Image as Image
import io
from array import array
from app import logger


# Функция проверки файла на соответствее его расширения допускаемым значениям
def is_allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Функция загрузки файла (POST запрос)
def upload_file(file, message_data):
    filename = secure_filename(file.filename)
    user = Users_repository.get_current_user(user_id=message_data['user_id'])
    # Генерация названия пути к файлу
    upload_path = f'{user.id}_{user.uuid}'

    # Создание пути к файлу (Если ещё не создан)
    if not os.path.exists(os.path.join(UPLOAD_FOLDER, upload_path)):
        os.mkdir(os.path.join(UPLOAD_FOLDER, upload_path))
    
    # Полный путь к файлу
    file_path = os.path.join(UPLOAD_FOLDER, upload_path, filename)
    
    # Создание записи о новом файле в БД
    Files_repository.create(message_data=message_data, file_path=file_path)

    # Сохранение файла по пути, заданному выше
    file.save(file_path)

    return jsonify({'message': 'file saved'})


# Функция записи чанка. offset - идентификатор последнего записанного байта
def chunk_upload(chunk: list, file_path: str, offset: int):
    try:
        # открытие файла в режиме добавления байтов
        with open(file_path, 'ab') as file:
            # переход к последнему байту
            file.seek(offset)
            # запись нового чанка с последнего байта
            file.write(bytearray(chunk))
            logger.info(f'CHUNK {offset} WRITED')

        return 'chunk uploaded'
    except Exception as e:
        print(e)
        return e
        


# функция загрузки файла по websocket протоколу
def convert_upload_file(data):
    try:
        logger.info('file getted')
        user = Users_repository.get_current_user(user_id=data['user_id'])
        # Генерация названия пути к файлу
        upload_path = f'{user.id}_{user.uuid}'
        print('user getted')

        # Создани директории для хранения файла (Если ещё не создана)
        if not os.path.exists(os.path.join(UPLOAD_FOLDER, upload_path)):
            os.mkdir(os.path.join(UPLOAD_FOLDER, upload_path))
        
        print('directory skiped')
        
        # (Если файл прошёл проверку по расширению)
        if is_allowed_file(data['file_name']):
            # Генерация полного пути к файлу 
            file_path = os.path.join(UPLOAD_FOLDER, upload_path, data['file_name'])

            # преобразование словаря в список байтов
            chunk = list(data['file'].values())

            # Запись чанка
            write_chunk = chunk_upload(chunk=chunk, file_path=file_path, offset=data['offset'])

            print('writed...')

            # Если чанк последний, то записываем данные о файле в БД и возвращаем абсолютный путь к нему
            # Иначе - возвращаем результат записи чанка
            if data['is_last_chunk'] == True:
                # Данные, необходимые для сохранения данных о файле в БД
                file_save_data = {
                    'user_id': data['user_id'],
                    'chat_id': data['chat_id']
                }

                Files_repository.create(message_data=file_save_data, file_path=file_path)

                return file_path
            else:
                return write_chunk

        else:
            return 'incorrect file type'
    except Exception as e:
        return e


# Получения списка всех файлов
def get_files_list():
    try:
        files = []

        for file in Files_repository.get_files_list():
            files.append(
                {   
                    'id': file.id,
                    'uuid': file.uuid,
                    'chat_id': file.chat_id,
                    'user_id': file.user_id,
                    'file_url': file.file_url,
                    'created_at': file.created_at,
                    'modified_at': file.modified_at
                }
            )

        return jsonify(files)
    except Exception as e:
        print(e)
        return jsonify({'message': 'error'})
    

# Получение информации о конкретном файле
def get_current_file(file_id):
    try:
        file = Files_repository.get_current_file(file_id=file_id)

        return jsonify({
            "id": file.id,
            "uuid": file.uuid,
            "chat_id": file.chat_id,
            "user_id": file.user_id,
            'file_url': file.file_url
        })
    except Exception as e:
        print(e)
        return jsonify({'message': 'error'})


# Обновление информации о конкретном файле (POST Запрос)
def update_file(message_data, file_id, file):
    try:
        # Получения имени файла (неизменно, привязано к файлу)
        filename = secure_filename(file.filename)
        # Получение данных о пользователе, отправившем файл
        user = Users_repository.get_current_user(user_id=message_data['user_id'])
        # Генерация названия директории для хранения файла
        upload_path = f'{user.id}_{user.uuid}'

        # Создание директории для хранения файла (Если ещё не создана)
        if not os.path.exists(os.path.join(UPLOAD_FOLDER, upload_path)):
            os.mkdir(os.path.join(UPLOAD_FOLDER, upload_path))
        
        # Запись файла по определённому пути
        file_path = os.path.join(UPLOAD_FOLDER, upload_path, filename)
        file.save(file_path)

        return Files_repository.update_file(message_data=message_data, file_id=file_id, file_path=file_path)
    except Exception as e:
        print(e)
        return jsonify({'message': 'error'})


# Функция удаления конкретного файла
def delete_file(file_id):
    try:
        return Files_repository.delete_file(file_id=file_id)
    except Exception as e:
        print(e)
        return jsonify({'message': 'error'})