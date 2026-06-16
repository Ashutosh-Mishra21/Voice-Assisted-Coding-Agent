from rank_bm25 import BM25Okapi


class BM25Indexer:

    def build(
        self,
        chunks,
    ):

        corpus = []

        for chunk in chunks:

            text = f"{chunk.symbol_name} " f"{chunk.content}"

            text = text.lower().split()

            corpus.append(text)

        bm25 = BM25Okapi(corpus)

        return bm25
