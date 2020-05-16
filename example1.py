#!/usr/bin/env python3

from collections import Counter
from itertools import islice

from gnt_data import ChunkType, TokenType, get_tokens, get_tokens_by_chunk
from sequencing_tools.ordering import frequency, frequency_optimised, next_best

# for GNT data, we can get our target-item data from the `gnt_data` module.
# so imagine we wanted to use lemmas as items and sentences as targets:

item_type = TokenType.lemma
target_type = ChunkType.verse

target_items = get_tokens_by_chunk(item_type, target_type)

def get_text(chunk_type, chunk_id):
    return " ".join(get_tokens(TokenType.text, target_type, target))


# items in John's Gospel

gjohn_items = set(Counter(get_tokens(item_type, ChunkType.book, "64")).keys())


# frequency

for target, items_to_learn in islice(frequency(target_items), 5):
    print(target, get_text(target_type, target))
    print(items_to_learn)

print()

for target, items_to_learn in islice(frequency(target_items, gjohn_items), 5):
    print(target, get_text(target_type, target))
    print(items_to_learn)

print()

for target, items_to_learn in islice(frequency(target_items, gjohn_items, True), 5):
    print(target, get_text(target_type, target))
    print(items_to_learn)

# print()

# for target, items_to_learn in islice(frequency_optimised(target_items), 10):
#     print(target, get_text(target_type, target))
#     print(items_to_learn)

# print()

# for target, items_to_learn in islice(next_best(target_items), 10):
#     print(target, get_text(target_type, target))
#     print(items_to_learn)
