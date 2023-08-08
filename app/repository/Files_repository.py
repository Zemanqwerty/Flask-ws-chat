from app import db
from ..models.File import Files
from ..models.Chat import Chats


# Функция Создания записи о файле
def create(message_data, file_path):
    # получение чата для проверки, находится ли пользователь в нужном чате
    chat = db.session.query(Chats).filter(Chats.id==message_data['chat_id']).first()
    # проверка наличия пользователя в чате
    if int(message_data['user_id']) == int(chat.user_id1) or int(message_data['user_id']) == int(chat.user_id2):
        # Создание записи о файле
        file = Files(chat_id=message_data['chat_id'], user_id=message_data['user_id'], file_url=file_path)
        db.session.add(file)
        db.session.commit()

        return f'file saved'
    else:
        return f'user {message_data.user_id} not in chat'


# Функция получения списка всех файлов
def get_files_list():
    files = Files.query.all()
    return files


# Получение информации о конкретном файле
def get_current_file(file_id):
    file = db.session.query(Files).filter(Files.id==file_id).first()
    return file


# Функция обновления информации о конкретном файле
def update_file(message_data, file_path, file_id):
    file = db.session.query(Files).filter(Files.id==file_id).first()
    
    # переопределение информации о файле
    file.chat_id = message_data['chat_id']
    file.user_id = message_data['user_id']
    file.file_url = file_path

    db.session.commit()
    return f'file updated'


# Функция удаления конкретного файла
def delete_file(file_id):
    file = Files.query.filter_by(id=file_id).delete()
    db.session.commit()

    return f'message with id {file_id} deleted'