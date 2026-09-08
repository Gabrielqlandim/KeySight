import httpx
from app.config import settings

BASE_URL = "https://api.isthereanydeal.com"

class ITADClientError(Exception):
    pass


async def lookup_game_id(title: str) ->str | None:
    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            response = await client.get(
                f"{BASE_URL}/games/lookup/v1",
                params={"key": settings.itad_api_key, "title": title},
            )
            response.raise_for_status()
        except httpx.TimeoutException:
            raise ITADClientError("Tempo esgotado ao consultar a api do ITAD")
        except httpx.HTTPStatusError as exc:
            raise ITADClientError(
                f"ITAD retornou erro {exc.response.status_code}"
            )

    data = response.json()
    if not data.get("found"):
        return None
    return data["game"]["id"]

async def get_current_prices(itad_game_id: str, country: str = "BR") -> list[dict]:
    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            response = await client.post(
                f"{BASE_URL}/games/prices/v3",
                params={"key": settings.itad_api_key, "country": country},
                json=[itad_game_id],
            )
            response.raise_for_status()
        except httpx.TimeoutException:
            raise ITADClientError("Tempo esgotado ao consultar API do ITAD")
        except httpx.HTTPStatusError as exc:
            raise ITADClientError(
                f"ITAD retornou erro {exc.response.status_code}"
            )

    data = response.json()
    if not data:
        return []
    return data[0].get("deals", [])