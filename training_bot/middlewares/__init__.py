from middlewares.sync_data import SyncDataMiddleware
from middlewares.log_updates import LogUpdateMiddleware
from middlewares.day_update import DayUpdateMiddleware


def setup_middlewares(dp):
    dp.update.outer_middleware(SyncDataMiddleware())
    dp.update.outer_middleware(LogUpdateMiddleware())
    dp.update.outer_middleware(DayUpdateMiddleware())
