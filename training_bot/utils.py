import asyncio
from calculator import GoalCalculator
from clients.weather import WeatherAPIClient


def format_user_profile(data):
    return f"""Ваш профиль:
    Вес: {data["weight"]} кг
    Рост: {data["height"]} см
    Возраст: {data["age"]} лет
    Активность: {data["activity"]} минут в день
    Цель: {int(data["goal_calories"])} ккал
    Пол: {"М" if data["gender"] == "мужской" else "Ж"}
    Город: {data["city"]}
"""


def get_start_message():
    return """Добро пожаловать! Я бот для расчета калорий и дневной нормы воды.
Введите /help для списка команд.
"""


def get_help_message():
    return """Доступные команды:
/start - Начало работы
/help - Список команд
/set_profile - Начать настройку профиля
/log_water <кол-во мл.> - Зафиксировать выпитую воду
/log_food <название продукта> - Зафиксировать прием пищи
/log_workout <вид тренировки> <время в минутах> - Зафиксировать тренировку
/check_progress - Проверить прогресс по воде и калориям
"""


async def calculate_goals(data, weather_client: WeatherAPIClient, goal_calories=None):
    goal_calculator = GoalCalculator()
    current_temp = await weather_client.async_get_day_temperature(data["city"])

    if goal_calories is None:
        goal_calories = goal_calculator.calculate_user_calories_goal(data)
    goal_water = goal_calculator.calculate_user_water_goal(data, current_temp)

    return goal_calories, goal_water
