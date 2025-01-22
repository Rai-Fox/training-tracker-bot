import httpx
import logging

logger = logging.getLogger(__name__)


class WeatherAPIClient:
    BASE_PATH = "https://api.openweathermap.org"

    def __init__(self, api_key):
        self.api_key = api_key
        self.async_client = httpx.AsyncClient()

    async def async_get_day_temperature(self, city_name):
        try:
            response = await self.async_client.get(
                f"{self.BASE_PATH}/data/2.5/weather",
                params={"q": city_name, "appid": self.api_key},
            )
            print(response.text)
            response.raise_for_status()
            return response.json()["main"]["temp"]
        except Exception as e:
            logger.error(f"Error while getting weather: {e}")
            raise
