    This is a literate doctest.
    Run ``python -m doctest example4.rst`` to test.


>>> from collections import Counter
>>> from itertools import islice

>>> from gnt_data import get_token_dicts, get_tokens_by_chunk, ChunkType, TokenType

>>> from sequencing_tools.model import LearningModel
>>> from sequencing_tools.ordering import next_best


>>> def chapter(chapter_id):
...     return get_token_dicts(ChunkType.chapter, chapter_id)


>>> def counter_filter(counter, condition):
...     return Counter({item:count for item, count in counter.items() if condition(count)})


>>> def john(chunk_type, token_type):
...     return get_tokens_by_chunk(token_type, chunk_type, condition=lambda chunk_id: chunk_id.startswith("64"))


Scenario #1
===========

>>> lm = LearningModel()

Say they've read John 1–3
-------------------------

>>> lm.read(chapter("6401"))
>>> lm.read(chapter("6402"))
>>> lm.read(chapter("6403"))

What are the twenty most common lemmas they've seen?
----------------------------------------------------

>>> print(lm.seen("lemma").most_common(20))
[('ὁ', 294), ('καί', 125), ('αὐτός', 104), ('εἰμί', 67), ('λέγω', 58), ('οὐ', 32), ('σύ', 32), ('ἐν', 28), ('ἐκ', 28), ('ἐγώ', 28), ('οὗτος', 27), ('Ἰησοῦς', 26), ('θεός', 25), ('ὅς', 24), ('ἔρχομαι', 23), ('ὅτι', 23), ('εἰς', 22), ('δέ', 20), ('πᾶς', 15), ('γίνομαι', 15)]

Which lemmas have they seen at least ten times?
------------------------------------------------

>>> print(counter_filter(lm.seen("lemma"), lambda count: count >= 10))
Counter({'ὁ': 294, 'καί': 125, 'αὐτός': 104, 'εἰμί': 67, 'λέγω': 58, 'οὐ': 32, 'σύ': 32, 'ἐν': 28, 'ἐκ': 28, 'ἐγώ': 28, 'οὗτος': 27, 'Ἰησοῦς': 26, 'θεός': 25, 'ὅς': 24, 'ἔρχομαι': 23, 'ὅτι': 23, 'εἰς': 22, 'δέ': 20, 'πᾶς': 15, 'γίνομαι': 15, 'πιστεύω': 15, 'ὁράω': 15, 'Ἰωάννης': 14, 'ἵνα': 14, 'ἄνθρωπος': 13, 'πρός': 12, 'ἀποκρίνομαι': 12, 'υἱός': 12, 'μή': 12, 'φῶς': 11, 'μαρτυρέω': 10, 'κόσμος': 10, 'βαπτίζω': 10})

How many complete sentences in John's Gospel contain only lemmas they've already seen?
--------------------------------------------------------------------------------------

>>> count = 0
>>> for sentence, lemmas in john(ChunkType.sentence, TokenType.lemma).items():
...     seen_count = len([x for x in lemmas if x in lm.seen("lemma")])
...     if seen_count / len(lemmas) == 1:
...         count += 1
>>> print(count)
311

What are the "next best" 5 verses for them to read from John's Gospel?
----------------------------------------------------------------------

>>> target_items = john(ChunkType.verse, TokenType.lemma)
>>> gen = next_best(target_items, items_already_known=lm.seen("lemma").keys())
>>> for target, items_to_learn in islice(gen, 5):
...     print(target, items_to_learn)
641223 {'δοξάζω'}
641228 set()
641331 set()
641705 set()
640531 {'ἐμαυτοῦ'}