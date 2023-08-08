from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from flask_socketio import SocketIO
import os
from app.middleware.formdata_validate import ValidateMiddleware
from flask_http_middleware import MiddlewareManager
from loguru import logger
from flask_sock import Sock


# Определение корневой директории
BASEDIR = os.path.abspath(os.path.dirname(__file__))

# Определение логгера
logger.add('debug.log', format='{time} {level} {message}', level='DEBUG')

# Определение приложения
app = Flask(__name__)
app.config.from_object('config.DevelopConfig')

# Определение слоя middleware (Не используется)
app.wsgi_app = MiddlewareManager(app)
app.wsgi_app.add_middleware(ValidateMiddleware)


db = SQLAlchemy(app)

Session(app)

# socketio = SocketIO(app, manage_session=False)
sock = Sock(app)

socket_clients_list = {}

# Определение корневого пути для записи файлов
UPLOAD_FOLDER = os.path.join(BASEDIR, 'files/users/')
# Определение допустимых расширения для файлов
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'docx'}

# подключение всех функционирующих файлов (необходимо определить для конкретной работы приложения)
from app.models import Chat, User, Messages, File
from app.views import Users_views, Chat_views, Messages_views, socket_chat_views, Files_views