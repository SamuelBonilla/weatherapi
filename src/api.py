import os
import aioredis
import requests
from datetime import datetime
from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import Response

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache


app = FastAPI()


@app.get("/weather")
@cache(expire=120)
async def index(city: str, country: str):
    url = f"{os.getenv('URL')}?q={city},{country}&appid={os.getenv('API_KEY')}"
    r = requests.get(url)
    data = r.json()
    if r.status_code != 200:
        return data
    response_format =  {
        "location_name": f"{data.get('name')}, {data.get('sys', {}).get('country')}",
        "temperature": f"{int(data.get('main', {}).get('temp', 273.15) - 273.15)} °C",
        "wind": f"Gentle breeze, {data.get('wind', {}).get('speed')} m/s, west-northwest",
        "cloudiness": f"{data.get('clouds', {}).get('all')}% clouds",
        "pressure": f"{data.get('main', {}).get('pressure')} hpa",
        "humidity": f"{data.get('main', {}).get('humidity')}%",
        "sunrise": f"{datetime.utcfromtimestamp(data.get('sys', {}).get('sunrise', 0)).strftime('%H:%M')}",
        "sunset": f"{datetime.utcfromtimestamp(data.get('sys', {}).get('sunset', 0)).strftime('%H:%M')}",
        "geo_coordinates": [data.get('coord', {}).get('lat'), data.get('coord', {}).get('lon')],
        "requested_time": f"{datetime.utcfromtimestamp(data.get('dt', 0)).strftime('%Y-%m-%d %H:%M:%S')}",
        "forecast": data.get('main', {})
    }
    return response_format


@app.on_event("startup")
async def startup():
    redis = await aioredis.create_redis_pool(os.getenv("REDIS_URL", "redis://localhost"), encoding="utf8")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")