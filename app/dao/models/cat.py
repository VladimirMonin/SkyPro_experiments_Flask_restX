from marshmallow import Schema, fields
from app.database import *  # Было db - стало all - чтобы импорт relationship тоже притянулся


class Cat(db.Model):  # Создаем таблицу с котиками
    __tablename__ = 'cat'

    def __repr__(self):  # Делаем описание объекта класса
        return f'Тип объекта: Котик. ' \
               f'ID: "{self.id}" ' \
               f'Имя: {self.name}'

    id = db.Column(db.Integer, primary_key=True)  # Первичный ключ. Автоинкремент НЕ включается по умолчанию
    name = db.Column(db.String)
    id_shop = db.Column(db.Integer, db.ForeignKey('shop.id'))  # Будет ссылочка на ID магазина

    shop = relationship('Shop')  # Настраиваем "отношения" с таблицей магазинов


class CatSchema(Schema):  # Делаем схему для таблицы котиков
    id = fields.Int(dump_only=True)
    name = fields.Str()
    id_shop = fields.Int()

    cat = relationship('Cat', overlaps='shop')  # Настраиваем отношения с таблицей котиков

