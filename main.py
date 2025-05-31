from fastapi import FastAPI
from dotenv import load_dotenv
from os import getenv

load_dotenv('.env')

app = FastAPI()


@app.get("/health")
async def check_health():
    return {
        'health': 'ok'
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, "127.0.0.1", port=getenv("PORT"))
