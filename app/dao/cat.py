#  Можно импортировать сессию из database тут, но внутрь класса интереснее
#  Потому что потом можем перевести каждый класс на разные базы данных. БОЛЕЕ ГИБКО

# CRUD - создание чтение обновление удаление
from app.dao.models.cat import Cat


class CatDAO:
    def __init__(self, session):
        self.session = session

    def get_one(self, cid):
        return self.session.query(Cat).get(cid)

    def get_all(self):
        return self.session.query(Cat).all()  # Запрос в модель алхимии Cat

    def create(self, data):
        cat = Cat(**data)

        self.session.add(cat)
        self.session.commit()

        return cat

    def update(self, cat):

        self.session.add(cat)
        self.session.commit()

        return cat

    def delete(self, cid):
        cat = self.get_one(cid)
        self.session.delete(cat)
        self.session.commit()
