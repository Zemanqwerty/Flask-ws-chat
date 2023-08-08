from app import app, db

# Создание необходимых таблиц (Если ещё не созданы)
app.app_context().push()
db.create_all()

# Запуск приложения
app.run(port=5001, debug=True)