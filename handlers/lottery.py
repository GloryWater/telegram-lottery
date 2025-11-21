import os
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import asyncpg

from handlers.start import keyboard_builder

lottery_router = Router(name=__name__)


class LotteryStates(StatesGroup):
    entering_recipe = State()


@lottery_router.callback_query(F.data == "view_my_codes")
async def view_my_codes_handler(callback: CallbackQuery, ):
    conn = await asyncpg.connect(user=os.getenv("DB_USER"), password=os.getenv("DB_PASSWORD"),
                                 database='gloryLottery', host='127.0.0.1')
    result = await conn.fetch("SELECT value FROM listofcodes WHERE activatedbyuserid = $1", callback.from_user.id)
    if result:
        codes = "Зарегистрированные Вами коды:\n"
        for i in range(len(result)):
            codes += f"{i+1}. {result[i][0]}\n"
        await callback.message.answer(codes, reply_markup=keyboard_builder(False))
    else:
        await callback.message.answer("Пока что Вы не зарегистрировали ни одного чека и поэтому не участвуете в розыгрыше 😢.",
                                      reply_markup=keyboard_builder(False))
    await conn.close()


@lottery_router.callback_query(F.data == "start_participating")
async def lottery_main_handler(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(LotteryStates.entering_recipe)
    await callback.message.answer(text="Введите уникальный код из Вашего чека ниже⬇️")


@lottery_router.message(LotteryStates.entering_recipe)
async def lottery_recipe_entered(message: Message, state: FSMContext) -> None:
    await state.clear()
    answer = ""
    conn = await asyncpg.connect(user=os.getenv("DB_USER"), password=os.getenv("DB_PASSWORD"),
                                 database='gloryLottery', host='127.0.0.1')
    selection = await conn.fetchrow("SELECT activatedbyuserid FROM listofcodes WHERE value = $1", message.text)
    if selection:
        if selection[0] == message.from_user.id:
            answer = "Вы уже зарегистрировали этот чек!"
        elif selection[0] == 0:
            answer = "Чек успешно зарегистрирован в розыгрыше. Если Ваш чек окажется победным, мы Вас оповестим."\
                     "\nЕсть ещё чеки? - Регистрируй дальше!"
            await conn.execute("UPDATE listofcodes SET activatedbyuserid = $1 WHERE value = $2 ", message.from_user.id, message.text)
        else:
            answer = "Чек уже кем-то зарегистрирован в розыгрыше!"
    else:
        answer = "Вы ввели несуществующий код!"
    await message.answer(answer, reply_markup=keyboard_builder())
    await conn.close()
