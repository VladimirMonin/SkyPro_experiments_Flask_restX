from flask import Flask  # Импортируем Flask - нет времени объяснять, просто делай)

from sqlalchemy.orm import relationship  # Импортируем "отношения" для джоинов в Алхимии
from sqlalchemy import or_, desc, func  # Импортируем доп. функции которые могут пригодится
from marshmallow import Schema, fields  # Имортируем Зефир. Для сериализации/десериализации объектов
from flask import request, jsonify
from flask_restx import Resource, Api
import json

from app.config import Config
from app.database import db


def create_app(config: Config) -> Flask:
    application = Flask(__name__)  # Создаем приложение
    application.config.from_object(config)  # Конфигурируем приложение
    application.app_context().push()  # Пушим настройки в приложение (у меня работало и так, но лучше не пропускать)

    return application


def configure_app(application: Flask):
    db.init_app(application)
    api = Api(app)
    api.add_namespace(None) # 'cats'



"""
Предыстория - вот что говорит вам предупреждение:

Flask-SQLAlchemy имеет собственную систему уведомлений о событиях, которая размещается поверх SQLAlchemy. 
Для этого он отслеживает изменения в сеансе SQLAlchemy. Это требует дополнительных ресурсов, поэтому опция 
SQLALCHEMY_TRACK_MODIFICATIONS позволяет отключить систему отслеживания изменений. В настоящее время опция по умолчанию 
имеет значение True, но в будущем это значение по умолчанию изменится на False, тем самым отключив систему событий.

Насколько я понимаю, обоснование изменения состоит из трех частей:
Не многие люди используют систему событий Flask-SQLAlchemy, но большинство людей не осознают, что могут сэкономить 
системные ресурсы, отключив ее. Поэтому разумнее по умолчанию отключить его, и те, кто хочет, могут включить его.
"""


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


class Shop(db.Model):  # Создаем таблицу с магазинами
    __tablename__ = 'shop'

    def __repr__(self):  # Делаем описание объекта класса
        return f'Тип объекта: Магазин. ' \
               f'Название: "{self.shop_title}" ' \
               f'ID: {self.id}'

    id = db.Column(db.Integer, primary_key=True)
    shop_title = db.Column(db.String)

    cat = relationship('Cat', overlaps='shop')  # Настраиваем отношения с таблицей котиков


db.create_all()

shop_1 = Shop(id=1, shop_title='Вселенная котиков')
shop_2 = Shop(id=2, shop_title='Котоны')
shop_3 = Shop(id=3, shop_title='Котопёс')

cat_1 = Cat(id=1, name='Барсик', id_shop=1)
cat_2 = Cat(id=2, name='Мурзик', id_shop=1)
cat_3 = Cat(id=3, name='Фёдор', id_shop=2)
cat_4 = Cat(id=4, name='Альбус', id_shop=2)
cat_5 = Cat(id=5, name='Бонифаций', id_shop=3)

cats = [cat_1, cat_2, cat_3, cat_4, cat_5]
shops = [shop_1, shop_2, shop_3]

db.session.add_all(cats)
db.session.add_all(shops)

db.session.commit()

# print(Shop.query.get(1))
# query = db.session.query(Cat.name, Shop.shop_title).join(Shop).all() # Сделали запрос всех котиков и подтянули с другой таблы магазины
# query = db.session.query(Cat.name, Cat.id, Shop.shop_title).join(Shop).filter(Cat.id.in_([1, 2])) # фильтр по ID котиков
query = db.session.query(Cat.name, Cat.id, Shop.shop_title).filter(Cat.name == 'Альбус',
                                                                   Shop.shop_title == 'Котоны').join(
    Shop)  # Параметр outer=True дает левый джоин, по умолчанию иннер


# for cat in query.all(): # Фильтрацию ALL можно сделать как тут, так и выше, в самом запросе
# for cat in query:
#     print(cat)


# Схемы сериализации

class CatSchema(Schema):  # Делаем схему для таблицы котиков
    id = fields.Int(dump_only=True)
    name = fields.Str()
    id_shop = fields.Int()


class ShopSchema(Schema):  # Делаем схему для таблицы магазинов
    id = fields.Int(dump_only=True)
    shop_title = fields.Str()


cat_schema = CatSchema()
cats_schema = CatSchema(many=True)

shop_schema = ShopSchema()
shops_schema = ShopSchema(many=True)

# Тест ДЕСЕРИАЛИЗАЦИИ

cat_6_dict_str = '{"name": "Схемкин", "id_shop": 3}'  # Строка с котиком №6
cat_6_dict = cat_schema.loads(cat_6_dict_str)  # Превращаем его в словарь

cat_6 = Cat(**cat_6_dict)  # Создаем объект Алхимии

db.session.add(cat_6)  # Записываем
db.session.commit()  # Коммитим


# Тест СЕРИАЛИЗАЦИИ

# cat_6 = db.session.query(Cat).filter(Cat.id == 6).join(Shop).one()
# string = cat_schema.dump(cat_6)
# print(string)
# print(type(string))

# TODO Сделать вьюшки наследуемые от Resource (17.2)

@cat_ns.route('/')
class CatsView(Resource):
    def get(self):
        all_cats = Cat.query.all()
        return cats_schema.dump(all_cats), 200


if __name__ == '__main__':
    app_config = Config()  # Создаем объект кофигурации Фласк from app.config import Config
    app = create_app(app_config)  # Создаем приложение Фласк
    configure_app(app)
    app.run(debug=False)
