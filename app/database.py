from flask_sqlalchemy import SQLAlchemy  # Импортируем Алхимию для Фласка
from sqlalchemy.orm import relationship

db = SQLAlchemy()  # Создаем объект Алхимии (app тут уже не нужен не передаем его)