from clients.weather import WeatherAPIClient
from clients.food import OpenFoodFactsAPIClient
from config import get_config


def setup_clients(dp):
    dp["weather_client"] = WeatherAPIClient(get_config().OPENWEATHERMAP_API_TOKEN)
    dp["food_client"] = OpenFoodFactsAPIClient()
