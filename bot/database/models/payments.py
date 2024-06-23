from bot.database.engine import BaseModel

from peewee import *

from bot.database.models.groups import Groups


class Payments(BaseModel):

    class Meta:

        db_table = 'payments'

    id = IntegerField(primary_key=True)
    user_id = IntegerField()
    username = TextField()
    amount = FloatField()
    created_at = DateField()
    group_id = ForeignKeyField(Groups, backref='payments')
