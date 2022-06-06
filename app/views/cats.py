from flask_restx import Resource, Namespace

from app.container import cat_service
from app.database import db
from flask import request

from app.dao.models.cat import CatSchema
from app.dao.models.shop import ShopSchema

cat_ns = Namespace('cat')
cats_ns = Namespace('cats')

cat_schema = CatSchema()
cats_schema = CatSchema(many=True)

shop_schema = ShopSchema()
shops_schema = ShopSchema(many=True)


@cat_ns.route('/')
class CatView(Resource):
    def get(self):
        all_cats = cat_service.get_all()  # Пока убрал изначальный вариант Cat.query.all()
        return cats_schema.dump(all_cats), 200

    def post(self):
        request_json = request.json
        cat_service.create(request_json)

        return '', 201


@cats_ns.route('/<int:cid>/')
class CatsView(Resource):
    def get(self, cid: int):
        cat = cat_service.get_one(cid)
        return cat_schema.dump(cat), 200
# TODO Методы put patch НЕ РАБОТАЮТ. Остальноё всё ок. Надо найти баг)

    def put(self, cid):
        request_json = request.json
        request_json['id'] = int(cid)  # Добавляем ID из урла для передачи далее
        cat_service.update(request_json)
        return '', 204

    def patch(self, cid):
        request_json = request.json
        request_json['id'] = cid  # Добавляем ID из урла для передачи далее
        cat_service.update_partial(request_json)
        return '', 204

    def delete(self, cid: int):
        cat_service.delete(cid)
        return '', 204
