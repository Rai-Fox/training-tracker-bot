from aiogram.fsm.state import State, StatesGroup


class UserProfileState(StatesGroup):
    weight = State()
    height = State()
    age = State()
    activity = State()
    city = State()
    goal = State()
    gender = State()
