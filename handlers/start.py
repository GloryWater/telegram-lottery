from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.types.inline_keyboard_markup import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton

start_router = Router(name=__name__)


def keyboard_builder(isEnabledSecondButton: bool = True) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(
        text="Зарегистрировать чек",
        callback_data="start_participating"
    ))
    if isEnabledSecondButton:
        builder.row(InlineKeyboardButton(
            text="Мои чеки",
            callback_data="view_my_codes"
        ))
    return builder.as_markup()


@start_router.message(CommandStart)
async def message_handler(message: Message) -> None:
    await message.answer(text='Привет! Для участия в акции необходимо зарегистрировать чек. Нажми на кнопку ниже для начала.',
                         reply_markup=keyboard_builder())
