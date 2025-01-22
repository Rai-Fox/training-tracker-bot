from handlers.base import router as base_router
from handlers.set_profile import router as set_profile_router
from handlers.progress import router as progress_router


def setup_handlers(dp):
    dp.include_router(base_router)
    dp.include_router(set_profile_router)
    dp.include_router(progress_router)
