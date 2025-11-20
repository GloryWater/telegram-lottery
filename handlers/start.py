from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.types.inline_keyboard_markup import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton

start_router = Router(name=__name__)


def keyboard_builder() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(
        text="Учавствовать",
        callback_data="start_participating"
    ))
    return builder.as_markup()


@start_router.message(CommandStart)
async def message_handler(message: Message) -> None:
    await message.answer(text='Привет! Для участия в акции необходимо зарегистрировать чек. Нажми на кнопку ниже для начала.',
                         reply_markup=keyboard_builder())
