from models.base_model import BaseModel
import peewee as pw
from models.user import User
from playhouse.hybrid import hybrid_property


class Message(BaseModel):
    sender = pw.ForeignKeyField(User,backref="receivers")
    receiver = pw.ForeignKeyField(User,backref="senders")
    message = pw.TextField(null=False)

