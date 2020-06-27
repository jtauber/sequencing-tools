from collections import Counter


class LearningModel:

    def __init__(self):
        self._seen = []

        # initially just a set without any model of how well know the item is
        self._known_vocab = set()

    def read(self, token_dicts):
        self._seen.extend(token_dicts)

    def seen(self, key):
        return Counter([t[key] for t in self._seen])

    def learn_vocab(self, lemmas):
        self._known_vocab |= set(lemmas)

    def vocab_size(self):
        return len(self._known_vocab)

    def is_known(self, lemma):
        return lemma in self._known_vocab

    def known_subset(self, counter):
        """
        subset the given counter to the known keys
        """
        return Counter(dict([
            (k, v)
            for (k, v) in counter.items()
            if k in self._known_vocab
        ]))
