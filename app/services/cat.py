from app.dao.cat import CatDAO


class CatService:
    def __init__(self, dao: CatDAO):
        self.dao = dao

    def get_one(self, cid):
        return self.dao.get_one(cid)

    def get_all(self):
        return self.dao.get_all()
        pass

    def create(self, data):
        return self.dao.create(data)
        pass

    def update(self, data):
        cid = data.get('id')
        cat = self.get_one(cid)

        cat.name = data.get('name')
        cat.shop = data.get('shop')

        self.dao.update(cat)
        pass

    def update_partial(self, data):
        cid = data.get('id')
        cat = self.get_one(cid)
        if 'name' in data:
            cat.name = data.get('name')
        if 'shop' in data:
            cat.shop = data.get('shop')

        self.dao.update(cat)
        pass

    def delete(self, cid):
        self.dao.delete(cid)
        pass
