from fastapi import APIRouter, Request
from app.services.weather_service import fetch_weather
from app.services.currency_service import get_exchange_rate
from app.services.coordinates_service import search_city_by_name

router = APIRouter()

@router.get("/list_api")
async def list_api(request: Request):
    request.app.logger.info("API List Executed successfully")
    return {
        "weather_api": "/api/v1/weather?city=<cityname>",
        "currency_api": "/api/v1/currency?base=<base>&target=<target>",
        "coordinates_api": "/api/v1/coordinates?place=<name>",
    }

@router.get("/weather")
async def weather(city: str, request: Request):
    request.app.logger.info(f"Weather fetch initiated for {city}")
    return fetch_weather(city, request)

@router.get("/currency")
async def currency(base: str = "USD", target: str = "INR", request: Request = None):
    request.app.logger.info(f"Currency exchange from {base} to {target}")
    return get_exchange_rate(base, target, request)

@router.get("/coordinates")
async def coordinates(place: str, request: Request):
    request.app.logger.info(f"Coordinates fetching for {place}")
    return search_city_by_name(place, request)
