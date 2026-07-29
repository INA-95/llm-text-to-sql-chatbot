# Text-to-SQL prompt 생성

def build_prompt(
    question: str,
    schema: str,
) -> str:
    """Build a schema-aware Text-to-SQL prompt."""

    return f"""
You are an expert data analyst who writes SQLite queries.

Use only the tables and columns included in the database schema below.

Database schema:
{schema}

User question:
{question}

Rules:
1. Generate exactly one valid SQLite query.
2. Use only the provided tables and columns.
3. Generate a read-only query using SELECT or WITH.
4. Do not insert, update, delete, drop, alter, create, or modify data.
5. Return SQL only.
6. Do not include explanations.
7. Do not include Markdown code fences.
""".strip()