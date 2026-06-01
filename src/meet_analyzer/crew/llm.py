from crewai import LLM

DEFAULT_MODELS = {
    "bedrock": "bedrock/us.anthropic.claude-sonnet-4-20250514-v1:0",
    "anthropic": "anthropic/claude-sonnet-4-0",
    "openai": "openai/gpt-4o",
}


def create_llm(provider="bedrock", model=None):
    if model is None:
        model = DEFAULT_MODELS.get(provider)
        if model is None:
            raise ValueError(f"Unknown provider '{provider}'. Use one of: {list(DEFAULT_MODELS.keys())}")
    elif "/" not in model:
        model = f"{provider}/{model}"
    return LLM(model=model)
