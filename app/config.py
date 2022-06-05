class Config:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # Настраиваем приложение для работы в ОЗУ
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Выключаем параметр приводящий к сообщению об ошибке
    JSON_AS_ASCII = False  # Выключаем ASCII чтобы получать норм. символы через jsonify
    RESTX_JSON = {'ensure_ascii': False, 'indent': 2}  # Выключаем ASCII чтобы получать норм. символы через API
