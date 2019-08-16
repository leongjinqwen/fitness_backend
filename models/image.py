from models.base_model import BaseModel
import peewee as pw
from models.user import User
from playhouse.hybrid import hybrid_property
import os


class Image(BaseModel):
    image_path = pw.TextField(null=False)
    user = pw.ForeignKeyField(User, backref='images')
    

    @hybrid_property
    def image_url(self):
        return os.environ.get("S3_DOMAIN") + self.image_path
    

    