from aiogram import Router
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram import F

from states.user_profile import UserProfileState
from filters import (
    CorrectGoalFilter,
    CorrectWeightFilter,
    CorrectHeightFilter,
    CorrectAgeFilter,
    CorrectActivityFilter,
    CorrectGenderFilter,
)
from clients.weather import WeatherAPIClient
from utils import calculate_goals, format_user_profile

router = Router()


@router.message(Command("set_profile"))
async def cmd_set_profile(message: Message, state: FSMContext):
    await message.reply("Введите ваш вес (в кг)")
    await state.set_state(UserProfileState.weight)


@router.message(UserProfileState.weight, CorrectWeightFilter())
async def process_weight(message: Message, state: FSMContext):
    weight = int(message.text)
    await state.update_data(weight=weight)
    await message.reply("Введите ваш рост (в см)")
    await state.set_state(UserProfileState.height)


@router.message(UserProfileState.weight)
async def process_incorrect_weight(message: Message):
    await message.reply("Вы ввели некорректный вес. Попробуйте еще раз.")
    await message.reply("Введите ваш вес (в кг)")


@router.message(UserProfileState.height, CorrectHeightFilter())
async def process_height(message: Message, state: FSMContext):
    height = int(message.text)
    await state.update_data(height=height)
    await message.reply("Введите ваш возраст (от 10 до 100 лет)")
    await state.set_state(UserProfileState.age)


@router.message(UserProfileState.height)
async def process_incorrect_height(message: Message):
    await message.reply("Вы ввели некорректный рост. Попробуйте еще раз.")
    await message.reply("Введите ваш рост (в см)")


@router.message(UserProfileState.age, CorrectAgeFilter())
async def process_age(message: Message, state: FSMContext):
    age = int(message.text)
    await state.update_data(age=age)
    await message.reply("Введите ваш уровень активности (в минутах в день)")
    await state.set_state(UserProfileState.activity)


@router.message(UserProfileState.age)
async def process_incorrect_age(message: Message):
    await message.reply("Вы ввели некорректный возраст. Попробуйте еще раз.")
    await message.reply("Введите ваш возраст (от 10 до 100 лет)")


@router.message(UserProfileState.activity, CorrectActivityFilter())
async def process_activity(message: Message, state: FSMContext):
    activity = int(message.text)
    await state.update_data(activity=activity)
    await message.reply("В каком городе вы находитесь?")
    await state.set_state(UserProfileState.city)


@router.message(UserProfileState.activity)
async def process_incorrect_activity(message: Message):
    await message.reply("Вы ввели некорректный уровень активности. Попробуйте еще раз.")
    await message.reply("Введите ваш уровень активности (в минутах в день)")


@router.message(UserProfileState.city)  # TODO: Add filter for city
async def process_city(message: Message, state: FSMContext):
    await state.update_data(city=message.text)
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Мужской")],
            [KeyboardButton(text="Женский")],
        ]
    )
    await message.reply("Введите ваш пол (мужской/женский)", reply_markup=keyboard)
    await state.set_state(UserProfileState.gender)


@router.message(UserProfileState.gender, CorrectGenderFilter())
async def process_gender(message: Message, state: FSMContext):
    await state.update_data(gender=message.text.lower())
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Рассчитать")],
        ]
    )
    await message.reply("Введите вашу цель (в ккал)", reply_markup=keyboard)
    await state.set_state(UserProfileState.goal)


@router.message(UserProfileState.gender)
async def process_incorrect_gender(message: Message):
    await message.reply("Вы ввели некорректный пол. Попробуйте еще раз.")
    await message.reply("Введите ваш пол (мужской/женский)")


@router.message(UserProfileState.goal, F.text.lower() == "рассчитать")
async def process_calc_goal(message: Message, state: FSMContext, weather_client: WeatherAPIClient):
    data = await state.get_data()

    goal_calories, goal_water = await calculate_goals(data, weather_client=weather_client)

    await state.update_data(goal_calories=goal_calories)
    await state.update_data(goal_water=goal_water)
    await state.update_data(profile_set=True)
    data = await state.get_data()
    await message.reply(format_user_profile(data))
    await state.set_state(None)


@router.message(UserProfileState.goal, CorrectGoalFilter())
async def process_user_goal(message: Message, state: FSMContext, weather_client: WeatherAPIClient):
    data = await state.get_data()

    goal_calories = int(message.text)
    goal_calories, goal_water = await calculate_goals(data, goal_calories=goal_calories, weather_client=weather_client)

    await state.update_data(goal_set_by_user=True)
    await state.update_data(goal_calories=goal_calories)
    await state.update_data(goal_water=goal_water)
    await state.update_data(profile_set=True)
    data = await state.get_data()
    await message.reply(format_user_profile(data))
    await state.set_state(None)


@router.message(UserProfileState.goal)
async def process_incorrect_goal(message: Message):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Рассчитать")],
        ]
    )
    await message.reply("Вы ввели некорректную цель. Попробуйте еще раз.")
    await message.reply("Введите вашу цель (в ккал)", keyboard=keyboard)


def setup_handlers(dp):
    dp.include_router(router)
