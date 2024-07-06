from fastapi import FastAPI
from redis import Redis
from router.expenses import router_expenses
from router.users import router_users
from database.cache import get_redis_connection
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



app = FastAPI()
app.include_router(router_users)
app.include_router(router_expenses)


@app.on_event("shutdown")
def shutdown_event():
    redisdb = get_redis_connection()
    redisdb.close()


@app.on_event("startup")
async def startup_event():
    redisdb = get_redis_connection()
    try:
        if redisdb.ping():
            print("Redis is online")
        else:
            print("Couldnt start Redis")
    except ConnectionError:
        print("Couldnt start Redis")


@app.get("/")
async def main():
    return {"message": "Hello World"}
