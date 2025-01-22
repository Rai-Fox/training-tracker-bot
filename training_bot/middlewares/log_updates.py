from typing import Any, Callable, Dict, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
import logging

logger = logging.getLogger(__name__)


class LogUpdateMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        user_id = event.message.from_user.id
        message = event.message.text
        logger.info(f"User {user_id} sent message: {message}")
        result = await handler(event, data)
        return result
