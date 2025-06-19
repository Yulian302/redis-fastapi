from fastapi import FastAPI
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from routers.store import store
from models.user import User


load_dotenv('.env')

app = FastAPI()

# connection pool
connection_pool = create_engine(
    getenv("DB_URL"),
    echo=True, pool_size=5,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=3600
)

app.include_router(store)


@app.get("/health")
async def check_health():
    return {
        'health': 'ok'
    }


@app.post("/user")
async def create_user():
    try:
        with Session(connection_pool) as session:
            sample_user = User(
                name="yulian"
            )
            session.add(sample_user)
            session.commit()
        return JSONResponse({"status": "created"}, status_code=201)
    except ConnectionError as e:
        return JSONResponse({"error": "Database error"}, status_code=500)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app=app, host="127.0.0.1", port=getenv("PORT"))

# line 1
# line 2
