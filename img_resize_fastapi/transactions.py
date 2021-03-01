import redis

r = redis.Redis(host='localhost', port=6379, db=0)
def to_store(uuid, img_type):
    r.set(uuid, img_type)
    return True

def to_retrieve(uuid):
    return r.get(uuid)