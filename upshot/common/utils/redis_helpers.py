import redis
from django.conf import settings

# Initialize Redis client
redis_client = redis.StrictRedis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
    decode_responses=True,
)


def redis_get_key(key):
    """
    returns value or None
    """
    value = redis_client.get(key)
    return value


def redis_setkv(key, value):
    """
    key: redis key
    value: key value

    returns True or False as result of operation
    """
    is_set = redis_client.set(key, value)
    return is_set


def redis_get_keys():
    keys = redis_client.keys()
    return keys


def redis_set_kvt(key, value, time):
    """
    key: redis key
    value: key value
    time: seconds, how long the key is available

    returns True or False as result of operation
    """
    is_set = redis_client.setex(key, time, value)
    return is_set


def redis_remove_key(key):
    """
    returns False if key does not exist or removed already
    returns True if key existed and deleted by this function
    """
    is_deleted = bool(redis_client.delete(key))
    return is_deleted


def redis_set_dict(name, value_dict):
    """
    set a dict with name in redis using hset
    """
    is_set = redis_client.hset(name=name, mapping=value_dict)
    return is_set


def redis_get_dict_value(name, key):
    """
    name: name used in hset
    key: the key of dictionary which you want its value
    """
    value = redis_client.hget(name, key)
    return value


def redis_set_expire_seconds(name, seconds):
    expire_set = redis_client.expire(name, seconds)
    return expire_set


def redis_get_dict(name):
    """
    name: name used in hset
    key: the key of dictionary which you want its value
    """
    value_dict = redis_client.hgetall(name)
    return value_dict
