#!/usr/bin/env python3

from itertools import islice

from gnt_data import ChunkType, TokenType, get_tokens, get_tokens_by_chunk
from sequencing_tools.ordering import frequency, frequency_optimised, next_best

# for GNT data, we can get our target-item data from the `gnt_data` module.
# so imagine we wanted to use lemmas as items and sentences as targets:

item_type = TokenType.lemma
target_type = ChunkType.verse

target_items = get_tokens_by_chunk(item_type, target_type)


def get_text(chunk_type, chunk_id):
    return " ".join(get_tokens(TokenType.text, chunk_type, chunk_id))


for strategy in (frequency, frequency_optimised, next_best):
    print()
    print()
    print(strategy.__name__)
    print()

    for target, items_to_learn in islice(strategy(target_items), 3):
        print(target, get_text(target_type, target))
        print(items_to_learn)

    print()

    items_learnt = set()
    targets_seen = set()
    target, items_to_learn = next(strategy(target_items))
    print(target, get_text(target_type, target))
    print(items_to_learn)

    items_learnt.update(items_to_learn)
    targets_seen.update({target})
    target, items_to_learn = next(strategy(target_items, items_learnt, True))
    print(target, get_text(target_type, target))
    print(items_to_learn)

    print()

    items_learnt = set()
    targets_seen = set()
    target, items_to_learn = next(strategy(target_items))
    print(target, get_text(target_type, target))
    print(items_to_learn)

    items_learnt.update(items_to_learn)
    targets_seen.update({target})
    target, items_to_learn = next(
        strategy(target_items, items_learnt, True, targets_seen)
    )
    print(target, get_text(target_type, target))
    print(items_to_learn)
