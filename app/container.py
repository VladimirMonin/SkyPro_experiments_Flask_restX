from app.dao.cat import CatDAO
from app.database import db
from app.services.cat import CatService


cat_dao = CatDAO(db.session)
cat_service = CatService(cat_dao)
