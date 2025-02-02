class SentanceTransformerEmbedding(BaseEmbedding):
    def __init__(
        self,
        model_name: str,
        tokenizer: Optional[Callable] = None,
        device: Optional[str] = None,
    ) -> None:
        super().__init__(tokenizer)
        self._model_name = model_name
        self._model = SentenceTransformer(model_name, device=device)

    def _get_embedding(self, text: str) -> EMB_TYPE:
        return self._model.encode([text])[0]
