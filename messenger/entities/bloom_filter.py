import redis
import pickle
from bloom_filter2 import BloomFilter


REDIS_KEY = "bloom:messages"
MAX_ELEMENTS = 4_000_000
ERROR_RATE = 0.001


class BloomFilterRepository:

    def __init__(self):
        self.redis = redis.Redis(host='localhost', port=6379, db=0)

    def load(self):
        data = self.redis.get(REDIS_KEY)
        if data:
            return pickle.loads(data)
        return BloomFilter(max_elements=MAX_ELEMENTS, error_rate=ERROR_RATE)

    def save(self, bloom):
        self.redis.set(REDIS_KEY, pickle.dumps(bloom))

