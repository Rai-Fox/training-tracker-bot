from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram import F

from clients.food import OpenFoodFactsAPIClient

router = Router()


@router.message(Command("log_water"))
async def log_water(message: Message, command: CommandObject, state: FSMContext):
    if command.args is None:
        await message.reply("Вы не указали количество выпитой воды. Попробуйте еще раз. (Пример: /log_water 200)")
        return

    try:
        water = int(command.args)
    except ValueError:
        await message.reply("Количество воды должно быть числом. Попробуйте еще раз.")
        return

    data = await state.get_data()
    logged_water = data.get("logged_water", 0)
    await state.update_data({"logged_water": logged_water + water})

    await message.reply(
        f"Вы выпили {water} мл воды.\n"
        f"Всего выпито: {logged_water + water} мл.\n"
        f"Сегодня вам нужно выпить еще {data['goal_water'] - logged_water - water:.0f} мл.\n"
    )


@router.message(Command("log_food"))
async def log_food(message: Message, command: CommandObject, state: FSMContext, food_client: OpenFoodFactsAPIClient):
    if command.args is None:
        await message.reply("Вы не указали продукт. Попробуйте еще раз. (Пример: /log_food яблоко)")

    product_name = command.args
    product_info = await food_client.get_product_info(product_name)

    if product_info is None:
        await message.reply(f"Продукт {product_name} не найден.")
        return

    data = await state.get_data()
    logged_calories = data.get("logged_calories", 0)

    await state.update_data({"logged_calories": logged_calories + product_info["calories"]})

    await message.reply(
        f"Вы съели {product_info['name']}.\n"
        f"Энергетическая ценность: {product_info['calories']:.0f} ккал.\n"
        f"Всего съедено: {logged_calories + product_info['calories']:.0f} ккал.\n"
        f"Сегодня вам нужно съесть еще {data['goal_calories'] + logged_calories + product_info['calories']:.0f} ккал.\n"
    )


@router.message(Command("log_workout"))
async def log_workout(message: Message, command: CommandObject, state: FSMContext):
    if command.args is None:
        await message.reply(
            "Вы не указали тип и продолжительность тренировки. Попробуйте еще раз. (Пример: /log_workout бег 30)"
        )
        return

    try:
        workout_type, workout_duration = command.args.split(" ", maxsplit=1)
        try:
            workout_duration = int(workout_duration)
        except ValueError:
            await message.reply("Продолжительность тренировки должна быть числом. Попробуйте еще раз.")
            return
    except ValueError:
        await message.reply("Неверный формат ввода. Попробуйте еще раз. (Пример: /log_workout бег 30)")
        return

    data = await state.get_data()
    burned_calories = data.get("burned_calories", 0)
    goal_water = data.get("goal_water", 0)
    logged_water = data.get("logged_water", 0)
    await state.update_data({"burned_calories": burned_calories + workout_duration * 10})
    await state.update_data({"goal_water": goal_water + workout_duration * 200 / 30})

    await message.reply(
        f"Вы занимались {workout_type} {workout_duration} минут.\n"
        f"Сожжено калорий: {workout_duration * 10:.0f} ккал.\n"
        f"Всего сожжено: {burned_calories + workout_duration * 10:.0f} ккал. \n\n"
        f"Дополнительно нужно выпить {workout_duration * 200 / 30:.0f} мл воды.\n"
        f"Сегодня вам нужно выпить еще {goal_water - logged_water + workout_duration * 200 / 30:.0f} мл.\n"
    )


@router.message(Command("check_progress"))
async def check_progress(message: Message, state: FSMContext):
    data = await state.get_data()
    logged_calories = data.get("logged_calories", 0)
    burned_calories = data.get("burned_calories", 0)
    logged_water = data.get("logged_water", 0)
    goal_calories = data.get("goal_calories", 0)
    goal_water = data.get("goal_water", 0)
    await message.reply(
        f"Прогресс:\n\n"
        f"Вода:\n"
        f"Выпито: {logged_water:.0f} мл. из {goal_water:.0f}\n"
        f"Осталось выпить: {goal_water - logged_water:.0f} мл.\n\n"
        f"Калории:\n"
        f"Потреблено: {logged_calories:.0f} ккал из {goal_calories:.0f}.\n"
        f"Сожжено: {burned_calories:.0f} ккал.\n"
        f"Баланс: {logged_calories - burned_calories:.0f}\n"
    )
