import enum
import os.path

ChunkType = enum.Enum("ChunkType", "book chapter verse sentence paragraph pericope")
TokenType = enum.Enum("TokenType", "text form lemma hybrid")

chunk_data_filename = {
    ChunkType.book: "books.txt",
    ChunkType.chapter: "chapters.txt",
    ChunkType.verse: "verses.txt",
    ChunkType.sentence: "sentences.txt",
    ChunkType.paragraph: "paragraphs.txt",
    ChunkType.pericope: "pericopes.txt",
}


chunk_data = {}  # (chunk_type, chunk_id) -> (token_start, token_end)
chunk_ids = {}  # chunk_type -> [chunk_id]


def load_chunk_data():
    for chunk_type, filename in chunk_data_filename.items():
        chunk_ids[chunk_type] = []
        with open(os.path.join(os.path.dirname(__file__), filename)) as f:
            for line in f:
                chunk_id, token_start, token_end = line.strip().split()
                chunk_data[(chunk_type, chunk_id)] = (int(token_start), int(token_end))
                chunk_ids[chunk_type].append(chunk_id)


token_data = {}  # token_type -> [tokens]
token_dicts = []  # [{}]

def load_tokens():
    for token_type in TokenType:
        token_data[token_type] = []

    with open(os.path.join(os.path.dirname(__file__), "tokens.txt")) as f:
        for line in f:
            token_id, text, form, pos, tag1, tag2, lemma = line.strip().split()

            # assume token_ids are sequential
            # token data is stored separately like this because all the
            # initial applications involve just wanting one particular type of
            # token at a time
            token_data[TokenType.text].append(text)
            token_data[TokenType.form].append(form)
            token_data[TokenType.lemma].append(lemma)
            if pos[0] == "R":
                token_data[TokenType.hybrid].append(form)
            elif lemma == "εἰμί":
                token_data[TokenType.hybrid].append(form)
            elif pos[0] == "V":
                token_data[TokenType.hybrid].append(lemma + "_" + tag2[0])
            else:
                token_data[TokenType.hybrid].append(lemma)
            # however token dicts are also stored
            token_dicts.append({
                "token_id": token_id,
                "text": text,
                "form": form,
                "pos": pos,
                "tag1": tag1,
                "tag2": tag2,
                "lemma": lemma,
            })


load_chunk_data()
load_tokens()


def get_tokens(token_type, chunk_type=None, chunk_id=None):
    """
    Return a list of tokens of the given `token_type` from the chunk of type
    `chunk_type` with identifier `chunk_id`.

    If `chunk_type` and `chunk_id` are omitted (they must both be if one is)
    then all tokens are returned.

    e.g. `get_tokens(TokenType.lemma, ChunkType.verse, "640316")` means
    "get the lemma tokens from verse 640316"
    """

    if chunk_type and chunk_id:
        start, end = chunk_data[(chunk_type, chunk_id)]

        # assume token_ids are sequential starting with 1
        return token_data[token_type][start - 1 : end]  # noqa: E203

    elif chunk_type is None and chunk_id is None:
        return token_data[token_type]

    else:
        raise ValueError(
            "either both or neither of chunk_type and chunk_id must be provided"
        )


def get_token_dicts(chunk_type, chunk_id):
    """
    Return of list of dicts with all the token information from the chunk of
    type `chunk_type` with identifier `chunk_id`.

    e.g. `get_tokens(ChunkType.verse, "640316")` means "get all the token data
    for verse 640316"
    """
    start, end = chunk_data[(chunk_type, chunk_id)]

    # assume token_ids are sequential starting with 1
    return token_dicts[start - 1 : end]  # noqa: E203


def get_tokens_by_chunk(token_type, chunk_type, condition=lambda chunk_id: True):
    """
    Return a dictionary mapping the ids of chunks of the given `chunk_type` to
    a list of tokens of the type `token_type` in that chunk.

    e.g. `get_tokens_by_chunk(TokenType.lemma, ChunkType.chapter)` will return
    a dictionary with an entry for each chapter where the key is the chapter
    identifier and the value is a list of lemmas (with repetitions if they
    exist)
    """
    return {
        chunk_id: get_tokens(token_type, chunk_type, chunk_id)
        for chunk_id in chunk_ids[chunk_type]
        if condition(chunk_id)
    }


# for quick testing
if __name__ == "__main__":
    for token in get_tokens(TokenType.text, ChunkType.verse, "640316"):
        print(token)
    print(get_tokens_by_chunk(TokenType.lemma, ChunkType.verse)["640316"])
