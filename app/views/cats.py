from flask_restx import Resource, Namespace
from app.database import db
from flask import request

from app.dao.models.cat import CatSchema
from app.dao.models.shop import ShopSchema

cat_ns = Namespace('cats')

cat_schema = CatSchema()
cats_schema = CatSchema(many=True)

shop_schema = ShopSchema()
shops_schema = ShopSchema(many=True)


@cat_ns.route('/')
class CatsView(Resource):
    def get(self):
        all_cats = cat_dao.get_all()  # Пока убрал изначальный вариант Cat.query.all()
        return cats_schema.dump(all_cats), 200

    def post(self):
        request_json = request.json
        cat_dao.create(request_json)

        return '', 201


cat_ns.route('/<int:cid>')
class CatView(Resource):
    def get(self, cid: int):
        cat = cat_dao.get_one(cid)
        return cat_schema.dump(cat), 200

    def put(self, cid: int):
        request_json = request.json
        request_json['id'] = cid  # Добавляем ID из урла для передачи далее
        cat_dao.update(request_json)
        return '', 204

    def patch(self, cid: int):
        request_json = request.json
        request_json['id'] = cid  # Добавляем ID из урла для передачи далее
        cat_dao.update.partial(request_json)
        return '', 204

    def delete(self, cid: int):
        cat_dao.delete(cid)
        return '', 204
