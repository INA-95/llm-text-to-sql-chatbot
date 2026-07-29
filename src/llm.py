# OpenAI API 호출

from openai import OpenAI

from src.config import MODEL_NAME


client = OpenAI()


def generate_sql(prompt: str) -> str:
    """Generate SQL from a Text-to-SQL prompt using OpenAI."""

    response = client.responses.create(
        model=MODEL_NAME,
        input=prompt,
    )

    generated_text = response.output_text.strip()

    if not generated_text:
        raise ValueError(
            "OpenAI returned an empty response."
        )

    return generated_text