from models.base_model import BaseModel
import peewee as pw
from models.user import User
from playhouse.hybrid import hybrid_property


class Relationship(BaseModel):
    fan = pw.ForeignKeyField(User,backref="idols")
    idol = pw.ForeignKeyField(User,backref="fans")
    approved= pw.BooleanField()




















    # @hybrid_property
    # def fans(self):
    #     fans = User.select().join(Relationship,on=(User.id==Relationship.fan)).where(Relationship.idol == self.id)
    #     return fans
    
    # @hybrid_property
    # def idols(self):
    #     idols = User.select().join(Relationship,on=(User.id==Relationship.idol)).where(Relationship.fan == self.id)
    #     return idols