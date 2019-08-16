from models.base_model import BaseModel
import peewee as pw
from models.user import User


class Record(BaseModel):
    user = pw.ForeignKeyField(User,backref="records")
    weight = pw.FloatField(null=False)
    height = pw.FloatField(null=False)
    bmi = pw.FloatField(null=False)