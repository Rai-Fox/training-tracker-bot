from aiogram.filters import BaseFilter
from aiogram.types import Message
import aiohttp


class CorrectWeightFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        try:
            weight = float(message.text)
            return 20 <= weight <= 200
        except ValueError:
            return False


class CorrectHeightFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        try:
            height = float(message.text)
            return 100 <= height <= 250
        except ValueError:
            return False


class CorrectAgeFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        try:
            age = int(message.text)
            return 10 <= age <= 100
        except ValueError:
            return False


class CorrectActivityFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        try:
            activity = int(message.text)
            return 0 <= activity <= 1440
        except ValueError:
            return False


class CorrectGoalFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        try:
            goal_calories = int(message.text)
            return 0 <= goal_calories <= 10000
        except ValueError:
            return False


class CorrectGenderFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return message.text.lower() in ["мужской", "женский"]
    

