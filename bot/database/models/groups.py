from bot.database.engine import BaseModel

from peewee import *


class Groups(BaseModel):

    class Meta:

        db_table = 'groups'

    id = IntegerField(primary_key=True)

    group_id = IntegerField(unique=True, null=False)
    waiting_pay = IntegerField(default=0)
    about_pay = IntegerField(default=0)
    common_pay = IntegerField(default=0)
    paid = IntegerField(default=0)
    message_id = IntegerField()
    thread_id = IntegerField(null=True)

