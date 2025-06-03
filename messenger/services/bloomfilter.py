from ..entities import BloomFilterRepository


class BloomFilterService:
    def __init__(self):
        self.bloom = BloomFilterRepository().load()
        self.count = 0

    def add(self, item):
        if item not in self.bloom:
            self.bloom.add(item)
            self.count += 1

    def contains(self, item) -> bool:
        return item in self.bloom

    def is_empty(self) -> bool:
        return self.count == 0

    def clear(self):
        self.bloom = BloomFilterRepository().load()
        self.count = 0
