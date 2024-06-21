from peewee import *


db = SqliteDatabase('database.db')


class BaseModel(Model):

    class Meta:
        database = db
