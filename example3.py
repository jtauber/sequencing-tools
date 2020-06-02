#!/usr/bin/env python3

from itertools import islice

from gnt_data import ChunkType, TokenType, get_tokens, get_tokens_by_chunk, chunk_data
from sequencing_tools.ordering import next_best


item_type1 = TokenType.form
item_type2 = TokenType.lemma
item_type3 = TokenType.hybrid

target_type = ChunkType.sentence

target_items3 = get_tokens_by_chunk(item_type3, target_type, condition=lambda chunk_id: chunk_id.startswith("64"))


def get_text(chunk_type, chunk_id):
    return " ".join(get_tokens(TokenType.text, chunk_type, chunk_id))


items_already_known = [
    # "Ἰησοῦς",
    # "Ναζωραῖος",
    # "Φίλιππος",
    # "Σίμων",
    # "Πέτρος",
    # "Ἀνδρέας",
    # "Πιλᾶτος",


    # "λέγω_P",
    # "εἰμί",
    # "οἶδα_X",
    # "ἐγώ",
    # "με",
    # "καί",
    # "οὐ", "οὔ",  # @@@
    # "αὐτῷ",
    # "αὐτοῖς",
    # "τόν",
    # "λέγω_A",
    # "ἀποκρίνομαι_A",
    # "ἐκεῖνος",
    # "οὗτος",
    # "λέγω_I",
    # "ὅτι",

]

gen = next_best(target_items3, items_already_known=items_already_known, yield_already_known=True)

for target, items_to_learn in gen:  #islice(gen, 20):
    print()
    print(f"sent_{target}:")
    print("    token_range: {}-{}".format(*chunk_data[ChunkType.sentence, target]))
    print("    text:", get_text(target_type, target))
    print("    new:", items_to_learn)
