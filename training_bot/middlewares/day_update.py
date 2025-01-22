from typing import Any, Callable, Dict, Awaitable
from datetime import datetime
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

import json

from utils import calculate_goals


class DayUpdateMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        state = data.get("state")
        weather_client = data.get("weather_client")
        if state:
            state_data = await state.get_data()
            last_update = state_data.get("last_update")
            today = datetime.now().date()
            if last_update != today:
                state_data["last_update"] = today
                state_data["logged_water"] = 0
                state_data["logged_calories"] = 0
                if state_data.get("profile_set", False):
                    return await handler(event, data)
                if state_data.get("goal_set_by_user"):
                    goal_calories, goal_water = await calculate_goals(
                        state_data, goal_calories=state_data["goal_calories"], weather_client=weather_client
                    )
                else:
                    goal_calories, goal_water = await calculate_goals(state_data, weather_client=weather_client)
                state_data["goal_calories"] = goal_calories
                state_data["goal_water"] = goal_water
        return await handler(event, data)
