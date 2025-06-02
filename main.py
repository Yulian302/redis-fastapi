from fastapi import FastAPI
from dotenv import load_dotenv
from os import getenv

from routers.store import store


load_dotenv('.env')

app = FastAPI()
app.include_router(store)


@app.get("/health")
async def check_health():
    return {
        'health': 'ok'
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app=app, host="127.0.0.1", port=getenv("PORT"))
