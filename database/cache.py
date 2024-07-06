import json


import redis

class RedisConnection:
    _instance = None
    @staticmethod
    def get_instance():
        if RedisConnection._instance is None:
            RedisConnection()
        return RedisConnection._instance

    def __init__(self):
        if RedisConnection._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            self.connection = redis.Redis(host='localhost', port=1234, db=0)
            RedisConnection._instance = self

    def get_connection(self):
        return self.connection

def get_redis_connection():
    return RedisConnection.get_instance().get_connection()

def set_data(key: str, value: dict, expiration: int = 5000):
    redisdb = get_redis_connection()
    if redisdb.set(key, json.dumps(value), ex=expiration):
        print("Data set in cache")
    else:
        print("Data created in cache")


def get_data(key: str):
    redisdb = get_redis_connection()
    data = redisdb.get(key)
    if data:
        print("Data found in cache")
        return json.loads(data)
    else:
        print("Data not found in cache")

