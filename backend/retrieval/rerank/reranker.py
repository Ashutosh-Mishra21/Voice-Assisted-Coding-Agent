from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
)

import torch

from backend.config.settings import settings
from backend.models.retrieval_result import RetrievalResult
from backend.retrieval.rerank.reranker_result import RerankResult


class CrossEncoderReranker:

    def __init__(self):

        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        self.tokenizer = AutoTokenizer.from_pretrained(settings.RERANK_MODEL)

        self.model = AutoModelForSequenceClassification.from_pretrained(
            settings.RERANK_MODEL
        )

        self.model.to(self.device)
        self.model.eval()

    def rerank(
        self,
        query: str,
        results: list[RetrievalResult],
        top_k: int = 5,
    ) -> list[RerankResult]:

        if not results:
            return []

        pairs = [[query, result.content] for result in results]

        inputs = self.tokenizer(
            pairs,
            padding=True,
            truncation=True,
            return_tensors="pt",
            max_length=512,
        )

        inputs = {key: value.to(self.device) for key, value in inputs.items()}

        with torch.no_grad():

            logits = self.model(**inputs).logits.squeeze(-1)

        scores = logits.cpu().tolist()
        reranked = []

        for result, score in zip(results, scores):

            reranked.append(
                RerankResult(
                    chunk_id=result.chunk_id,
                    file_path=result.file_path,
                    symbol_name=result.symbol_name,
                    content=result.content,
                    retrieval_score=result.score,
                    rerank_score=float(score),
                    source=result.source,
                )
            )
        reranked.sort(
            key=lambda x: x.rerank_score,
            reverse=True,
        )

        return reranked[:top_k]
