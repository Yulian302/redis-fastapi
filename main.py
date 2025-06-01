from fastapi import FastAPI, Query
from dotenv import load_dotenv
from os import getenv

from pydantic import BaseModel
from redisClient import RawRedisClient


load_dotenv('.env')

app = FastAPI()
redis_client = RawRedisClient()


@app.get("/health")
async def check_health():
    return {
        'health': 'ok'
    }


class KeyValueModel(BaseModel):
    key: str
    value: int


@app.post("/set")
async def set_key(item: KeyValueModel):
    redis_client._send_redis_command("SET", item.key, item.value)
    return {
        "status": "success"
    }


@app.get("/get")
async def get_value(key: str = Query(...)):
    value = redis_client._send_redis_command('GET', key)
    return {
        "value": value
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app=app, host="127.0.0.1", port=getenv("PORT"))
