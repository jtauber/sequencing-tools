    This is a literate doctest.
    Run ``python -m doctest example5.rst`` to test.

Augmenting a Textbook
=====================

Say our primary sequence is determined by a traditional textbook but we want to track vocabulary coverage, find readable sentences, or small gaps to fill so we get more readable sentences.

(This is very much exploratory and a work-in-progress. Code will be moved from here in to libraries as things mature.)

>>> from itertools import islice

>>> from sequencing_tools.model import LearningModel
>>> from sequencing_tools.ordering import next_best

>>> from gnt_data import ChunkType, TokenType, get_tokens_by_chunk, get_tokens

This is just a helper method to display a text chunk.

>>> def get_text(chunk_type, chunk_id):
...     return " ".join(get_tokens(TokenType.text, chunk_type, chunk_id))

We start off creating an empty learning model.

>>> lm = LearningModel()

Then we load a vocabulary list organized by chapter from a textbook (in this case, Croy).

>>> import croy
>>> croy_vocab_by_chapter = croy.load()

Let's assume the vocabulary the first five chapters has been learnt.

>>> for chapter in ["2", "3", "4", "5"]:
...     lm.learn_vocab(croy_vocab_by_chapter[chapter])

How many unique lemmas is this?

>>> print(lm.vocab_size())
73

How many tokens are there in the GNT with these lemmas?

>>> from collections import Counter
>>> gnt_lemma_counts = Counter(get_tokens(TokenType.lemma))
>>> known_lemma_counts = lm.known_subset(gnt_lemma_counts)
>>> round(100 * sum(known_lemma_counts.values()) / sum(gnt_lemma_counts.values()), 1)
35.9

In other words, 35.9% of tokens in the GNT.

What about just within each Gospel?

>>> for book in ["61", "62", "63", "64"]:
...     book_lemma_counts = Counter(get_tokens(TokenType.lemma, ChunkType.book, book))
...     known_book_lemma_counts = lm.known_subset(book_lemma_counts)
...     print(book, round(100 * sum(known_book_lemma_counts.values()) / sum(book_lemma_counts.values()), 1))
61 37.2
62 36.6
63 35.9
64 35.5

In other words, with the 73 vocabulary items in the first five Croy chapters, we've covered 37.2% of the tokens in Matthew, 36.6% of Mark, 35.9% of Luke, and 35.5% of John.

Of the lemmas we've learnt (from the first five Croy chapters), what is the least frequent in the GNT and how many times does it appear?

>>> known_lemma_counts.most_common()[-1]
('ἀδελφή', 25)

What are the 5 most frequent lemmas not covered by Croy in the first five chapters?

>>> top_5_left = (gnt_lemma_counts - known_lemma_counts).most_common(5)
>>> top_5_left
[('αὐτός', 5546), ('σύ', 2894), ('ἐν', 2733), ('ἐγώ', 2572), ('εἰμί', 2456)]

Imagine if we learnt those as well as the first five chapters:

>>> lm.learn_vocab(lemma for lemma, count in top_5_left)

With that addition, how many verses are readable at this point (just from a lemma point of view)?

>>> items_by_target = get_tokens_by_chunk(TokenType.lemma, ChunkType.verse)
>>> readable_targets = []
>>> for target, items in items_by_target.items():
...     known_count = sum(1 for item in items if lm.is_known(item))
...     if known_count == len(items):
...         readable_targets.append(target)
>>> len(readable_targets)
3

What about at the 90% level?

>>> readable_targets = []
>>> for target, items in items_by_target.items():
...     known_count = sum(1 for item in items if lm.is_known(item))
...     if known_count >= 0.9 * len(items):
...         readable_targets.append(target)
>>> len(readable_targets)
9

And what are they?

>>> for target in readable_targets:
...     print(target, get_text(ChunkType.verse, target))
630605 καὶ ἔλεγεν αὐτοῖς· Κύριός ἐστιν τοῦ σαββάτου ὁ υἱὸς τοῦ ἀνθρώπου.
632030 καὶ ὁ δεύτερος
640104 ἐν αὐτῷ ζωὴ ἦν, καὶ ἡ ζωὴ ἦν τὸ φῶς τῶν ἀνθρώπων·
640636 ἀλλ’ εἶπον ὑμῖν ὅτι καὶ ἑωράκατέ με καὶ οὐ πιστεύετε.
640669 καὶ ἡμεῖς πεπιστεύκαμεν καὶ ἐγνώκαμεν ὅτι σὺ εἶ ὁ ἅγιος τοῦ θεοῦ.
640845 ἐγὼ δὲ ὅτι τὴν ἀλήθειαν λέγω, οὐ πιστεύετέ μοι.
670420 οὐ γὰρ ἐν λόγῳ ἡ βασιλεία τοῦ θεοῦ ἀλλ’ ἐν δυνάμει.
690421 Λέγετέ μοι, οἱ ὑπὸ νόμον θέλοντες εἶναι, τὸν νόμον οὐκ ἀκούετε;
830512 ὁ ἔχων τὸν υἱὸν ἔχει τὴν ζωήν· ὁ μὴ ἔχων τὸν υἱὸν τοῦ θεοῦ τὴν ζωὴν οὐκ ἔχει.

What verses might be good to read next (just based on lemmas and the "next-best (2008)" algorithm)?

>>> gen = next_best(items_by_target, items_already_known=lm._known_vocab)
>>> for target, items_to_learn in islice(gen, 10):
...     print(target, get_text(ChunkType.verse, target))
...     print(sorted(items_to_learn))
830512 ὁ ἔχων τὸν υἱὸν ἔχει τὴν ζωήν· ὁ μὴ ἔχων τὸν υἱὸν τοῦ θεοῦ τὴν ζωὴν οὐκ ἔχει.
['μή']
670323 ὑμεῖς δὲ Χριστοῦ, Χριστὸς δὲ θεοῦ.
['Χριστός']
611615 λέγει αὐτοῖς· Ὑμεῖς δὲ τίνα με λέγετε εἶναι;
['τίς']
621036 ὁ δὲ εἶπεν αὐτοῖς· Τί θέλετε ποιήσω ὑμῖν;
['ποιέω']
640540 καὶ οὐ θέλετε ἐλθεῖν πρός με ἵνα ζωὴν ἔχητε.
['πρός', 'ἔρχομαι', 'ἵνα']
641034 ἀπεκρίθη αὐτοῖς ὁ Ἰησοῦς· Οὐκ ἔστιν γεγραμμένον ἐν τῷ νόμῳ ὑμῶν ὅτι Ἐγὼ εἶπα· Θεοί ἐστε;
['ἀποκρίνομαι', 'Ἰησοῦς']
641230 ἀπεκρίθη Ἰησοῦς καὶ εἶπεν· Οὐ δι’ ἐμὲ ἡ φωνὴ αὕτη γέγονεν ἀλλὰ δι’ ὑμᾶς.
['γίνομαι', 'διά', 'οὗτος']
640827 οὐκ ἔγνωσαν ὅτι τὸν πατέρα αὐτοῖς ἔλεγεν.
['πατήρ']
641037 εἰ οὐ ποιῶ τὰ ἔργα τοῦ πατρός μου, μὴ πιστεύετέ μοι·
['εἰ']
641411 πιστεύετέ μοι ὅτι ἐγὼ ἐν τῷ πατρὶ καὶ ὁ πατὴρ ἐν ἐμοί· εἰ δὲ μή, διὰ τὰ ἔργα αὐτὰ πιστεύετε.
[]
