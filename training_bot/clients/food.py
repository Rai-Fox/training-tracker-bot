import httpx
import logging

logger = logging.getLogger(__name__)


class OpenFoodFactsAPIClient:
    """
    Позволяет по названию продукта получить информацию о нем с сайта Open Food Facts
    """

    BASE_PATH = "https://world.openfoodfacts.org/"

    def __init__(self):
        self.async_client = httpx.AsyncClient()

    async def get_product_info(self, product_name: str):
        try:
            response = await self.async_client.get(
                f"{self.BASE_PATH}/cgi/search.pl",
                params={"search_terms": product_name, "action": "process", "json": "true"},
            )

            response.raise_for_status()
            data = response.json()
            products = data.get("products", [])
            if products:  # Проверяем, есть ли найденные продукты
                first_product = products[0]
                return {
                    "name": first_product.get("product_name", "Неизвестно"),
                    "calories": float(first_product.get("nutriments", {}).get("energy-kcal_100g", 0)),
                }

        except Exception as e:
            logger.error(f"Error while getting weather: {e}")
            raise
