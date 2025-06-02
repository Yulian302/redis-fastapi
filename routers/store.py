from fastapi.params import Query
from fastapi.routing import APIRouter

from models.KeyValue import KeyValueModel
from redisClient import RawRedisClient

redis_client = RawRedisClient()

store = APIRouter(prefix="/store")


@store.post("/set")
async def set_key(item: KeyValueModel):
    redis_client._send_redis_command("SET", item.key, item.value)
    return {
        "status": "success"
    }


@store.get("/get")
async def get_value(key: str = Query(...)):
    value = redis_client._send_redis_command('GET', key)
    return {
        "value": value
    }
