from models.base_model import BaseModel
import peewee as pw
from models.user import User


class Position(BaseModel):
    user = pw.ForeignKeyField(User,backref="position")
    lat = pw.TextField()
    lng = pw.TextField()
