from aiogram import F, Router
from aiogram.filters.chat_member_updated import \
    ChatMemberUpdatedFilter, IS_NOT_MEMBER, MEMBER, ADMINISTRATOR
from aiogram.fsm.context import FSMContext
from aiogram.types import ChatMemberUpdated

from bot.database.models.groups import Groups
from bot.database.models.payments import Payments
from bot.service.redis_serv.user import set_users_text

router = Router()
router.my_chat_member.filter(F.chat.type.in_({"group", "supergroup"}))


@router.my_chat_member(
    ChatMemberUpdatedFilter(
        member_status_changed=ADMINISTRATOR >> IS_NOT_MEMBER
    )
)
async def bot_deleted_as_admin(event: ChatMemberUpdated, state: FSMContext):

    await state.clear()
    delete_payments = Payments.delete().where(Payments.group_id == event.chat.id)
    delete_payments.execute()
    delete_group = Groups.delete().where(Groups.group_id == event.chat.id)
    delete_group.execute()
    await set_users_text(chat_id=event.chat.id, text="")
    print("Удалили")


@router.my_chat_member(
    ChatMemberUpdatedFilter(
        member_status_changed=MEMBER >> IS_NOT_MEMBER
    )
)
async def bot_deleted_as_member(event: ChatMemberUpdated):

    delete_payments = Payments.delete().where(Payments.group_id == event.chat.id)
    delete_payments.execute()
    delete_group = Groups.delete().where(Groups.group_id == event.chat.id)
    delete_group.execute()
    await set_users_text(chat_id=event.chat.id, text="")
    print("Удалили")
