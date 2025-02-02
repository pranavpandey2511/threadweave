from gpt4all import GPT4All


def _get_model(model_name: str = "orca-mini-3b.ggmlv3.q4_0.bin"):
    return GPT4All(model_name)


def _get_query_response(model, query: str, top_k: int = 5, device: str = "cpu"):
    output = model.generate(
        "The capital of France is ", max_tokens=3, device=device
    )
    return output
