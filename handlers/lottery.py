import os
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import asyncpg

lottery_router = Router(name=__name__)


class LotteryStates(StatesGroup):
    entering_recipe = State()


@lottery_router.callback_query(F.data == "start_participating")
async def lottery_main_handler(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(LotteryStates.entering_recipe)
    await callback.message.answer(text="Введите уникальный код из Вашего чека ниже⬇️")


@lottery_router.message(LotteryStates.entering_recipe)
async def lottery_recipe_entered(message: Message, state: FSMContext) -> None:
    await state.clear()
    conn = await asyncpg.connect(user=os.getenv("DB_USER"), password=os.getenv("DB_PASSWORD"),
                                 database='gloryLottery', host='127.0.0.1')
    selection = await conn.fetchrow("SELECT * FROM listofcodes WHERE value = $1", message.text)
    if selection:
        await conn.execute("UPDATE listofcodes SET activatedbyuserid = $1 WHERE value = $2 ",
                           message.from_user.id, message.text)
        await message.answer("Ваш чек зарегистрирован успешно!\nЕсть ещё чеки? - Регистрируй дальше!")
    else:
        await message.answer("Вы ввели код неправильно либо чек уже зарегистрирован.")
    await conn.close()
