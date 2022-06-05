from flask import Flask  # Импортируем Flask - нет времени объяснять, просто делай)
from flask_restx import Api


from app.config import Config
from app.database import db
from app.dao.models.cat import Cat, CatSchema
from app.dao.models.shop import Shop, ShopSchema
from app.views.cats import cat_ns, cats_ns


def create_app(config: Config) -> Flask:
    application = Flask(__name__)  # Создаем приложение
    application.config.from_object(config)  # Конфигурируем приложение
    application.app_context().push()  # Пушим настройки в приложение (у меня работало и так, но лучше не пропускать)
    return application


def configure_app(application: Flask):
    db.init_app(application)
    api = Api(app)
    api.add_namespace(cat_ns) # импорт из from app.views.cats import cat_ns
    api.add_namespace(cats_ns)

def create_data():

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

    db.create_all()

    with db.session.begin():
        db.session.add_all(cats)
        db.session.add_all(shops)

    #db.session.commit()

# print(Shop.query.get(1))
# query = db.session.query(Cat.name, Shop.shop_title).join(Shop).all() # Сделали запрос всех котиков и подтянули с другой таблы магазины
# query = db.session.query(Cat.name, Cat.id, Shop.shop_title).join(Shop).filter(Cat.id.in_([1, 2])) # фильтр по ID котиков
# query = db.session.query(Cat.name, Cat.id, Shop.shop_title).filter(Cat.name == 'Альбус', Shop.shop_title == 'Котоны').join(Shop)  # Параметр outer=True дает левый джоин, по умолчанию иннер
#
#
# for cat in query.all(): # Фильтрацию ALL можно сделать как тут, так и выше, в самом запросе
# for cat in query:
#     print(cat)
#
#
# Схемы сериализации
#
#
#
#
# Тест ДЕСЕРИАЛИЗАЦИИ
#
# cat_6_dict_str = '{"name": "Схемкин", "id_shop": 3}'  # Строка с котиком №6
# cat_6_dict = cat_schema.loads(cat_6_dict_str)  # Превращаем его в словарь
#
# cat_6 = Cat(**cat_6_dict)  # Создаем объект Алхимии
#
# db.session.add(cat_6)  # Записываем
# db.session.commit()  # Коммитим
#
#
# Тест СЕРИАЛИЗАЦИИ
#
# cat_6 = db.session.query(Cat).filter(Cat.id == 6).join(Shop).one()
# string = cat_schema.dump(cat_6)
# print(string)
# print(type(string))

if __name__ == '__main__':
    app_config = Config()  # Создаем объект кофигурации Фласк from app.config import Config
    app = create_app(app_config)  # Создаем приложение Фласк
    configure_app(app)
    create_data()
    app.run()
