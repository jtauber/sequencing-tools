#!/usr/bin/env python3

# for GNT data, we can get our target-item data from the `gnt_data` module.

from gnt_data import get_tokens_by_chunk, ChunkType, TokenType

# so imagine we wanted to use lemmas as items and sentences as targets:

target_items = get_tokens_by_chunk(TokenType.lemma, ChunkType.sentence)

from sequencing_tools.ordering import frequency, frequency_optimised, next_best

from itertools import islice

for target, items_to_learn in islice(frequency(target_items), 5):
    print(target)

print()

for target, items_to_learn in islice(frequency_optimised(target_items), 5):
    print(target)

print()

for target, items_to_learn in islice(next_best(target_items), 5):
    print(target)
