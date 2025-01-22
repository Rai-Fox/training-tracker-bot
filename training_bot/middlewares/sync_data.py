from typing import Any, Callable, Dict, Awaitable
from datetime import datetime
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

import json


class SyncDataMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        state = data.get("state")
        if state:
            state_data = await state.get_data()
            user_id = event.message.from_user.id
            if not state_data:
                try:
                    with open(f"users_data/{user_id}.json", "r") as file:
                        state_data = json.load(file)
                except FileNotFoundError:
                    state_data = {}
            await state.set_data(state_data)

        result = await handler(event, data)

        user_id = event.message.from_user.id
        if state:
            state_data = await state.get_data()
            with open(f"users_data/{user_id}.json", "w") as file:
                file.write(json.dumps(state_data))

        return result
