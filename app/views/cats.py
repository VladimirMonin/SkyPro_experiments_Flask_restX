from flask_restx import Resource, Namespace
from app.database import db
from flask import request

from app.models import CatSchema, ShopSchema, Cat

cat_ns = Namespace('cats')

cat_schema = CatSchema()
cats_schema = CatSchema(many=True)

shop_schema = ShopSchema()
shops_schema = ShopSchema(many=True)



@cat_ns.route('/')
class CatsView(Resource):
    def get(self):
        all_cats = db.session.query(Cat).all()  # Пока убрал изначальный вариант Cat.query.all()
        return cats_schema.dump(all_cats), 200

