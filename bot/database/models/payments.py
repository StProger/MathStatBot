from bot.database.engine import BaseModel

from peewee import *

from bot.database.models.groups import Groups


class Payments(BaseModel):

    class Meta:

        db_table = 'payments'

    id = IntegerField(primary_key=True)
    user_id = IntegerField()
    amount = FloatField()
    created_at = DateField(auto_now_add=True)
    group_id = ForeignKeyField(Groups, backref='payments')
