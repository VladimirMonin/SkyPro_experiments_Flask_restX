from marshmallow import Schema, fields
from app.database import *  # Было db - стало all - чтобы импорт relationship тоже притянулся


class Shop(db.Model):  # Создаем таблицу с магазинами
    __tablename__ = 'shop'

    def __repr__(self):  # Делаем описание объекта класса
        return f'Тип объекта: Магазин. ' \
               f'Название: "{self.shop_title}" ' \
               f'ID: {self.id}'

    id = db.Column(db.Integer, primary_key=True)
    shop_title = db.Column(db.String)


class ShopSchema(Schema):  # Делаем схему для таблицы магазинов
    id = fields.Int(dump_only=True)
    shop_title = fields.Str()
