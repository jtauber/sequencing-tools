from collections import Counter


class LearningModel:

    def __init__(self):
        self._seen = []

    def read(self, token_dicts):
        self._seen.extend(token_dicts)

    def seen(self, key):
        return Counter([t[key] for t in self._seen])
