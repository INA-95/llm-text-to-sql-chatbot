import re
import sqlite3
from pathlib import Path

import pandas as pd
from openai import OpenAI


DB_PATH = Path("data/sample.db")
MODEL_NAME = "gpt-5-mini"

client = OpenAI()


def get_database_schema(db_path: Path) -> str:
    schema_lines = []

    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
              AND name NOT LIKE 'sqlite_%'
            ORDER BY name;
        """)

        tables = [row[0] for row in cursor.fetchall()]

        for table_name in tables:
            schema_lines.append(f"Table: {table_name}")

            cursor.execute(f'PRAGMA table_info("{table_name}");')
            columns = cursor.fetchall()

            for column in columns:
                column_name = column[1]
                column_type = column[2] or "UNKNOWN"

                schema_lines.append(
                    f"- {column_name}: {column_type}"
                )

            schema_lines.append("")

    return "\n".join(schema_lines).strip()


def build_prompt(question: str, schema: str) -> str:
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
4. Do not insert, update, delete, drop, alter, or modify data.
5. Return SQL only.
6. Do not include explanations.
7. Do not include Markdown code fences.
""".strip()


def generate_sql(prompt: str) -> str:
    response = client.responses.create(
        model=MODEL_NAME,
        input=prompt,
    )

    return response.output_text.strip()


def clean_sql(raw_sql: str) -> str:
    sql = raw_sql.strip()

    sql = re.sub(
        r"^```(?:sql)?\s*",
        "",
        sql,
        flags=re.IGNORECASE,
    )
    sql = re.sub(r"\s*```$", "", sql)

    return sql.strip()


def validate_read_only_sql(sql: str) -> None:
    normalized_sql = " ".join(sql.lower().split())

    if not normalized_sql.startswith(("select ", "with ")):
        raise ValueError(
            "Only SELECT or WITH queries are allowed."
        )

    blocked_keywords = [
        "insert ",
        "update ",
        "delete ",
        "drop ",
        "alter ",
        "create ",
        "replace ",
        "truncate ",
        "attach ",
        "detach ",
        "vacuum ",
        "pragma ",
    ]

    for keyword in blocked_keywords:
        if keyword in normalized_sql:
            raise ValueError(
                f"Unsafe SQL keyword detected: {keyword.strip()}"
            )


def execute_sql(sql: str, db_path: Path) -> pd.DataFrame:
    with sqlite3.connect(db_path) as conn:
        return pd.read_sql_query(sql, conn)


def main() -> None:
    if not DB_PATH.exists():
        print(f"Database not found: {DB_PATH.resolve()}")
        return

    schema = get_database_schema(DB_PATH)

    print("Database schema:")
    print("-" * 60)
    print(schema)
    print("-" * 60)

    question = input(
        "\nAsk a question about the dataset: "
    ).strip()

    if not question:
        print("Question cannot be empty.")
        return

    try:
        prompt = build_prompt(question, schema)

        print("\nGenerating SQL with OpenAI...")

        raw_sql = generate_sql(prompt)
        generated_sql = clean_sql(raw_sql)

        validate_read_only_sql(generated_sql)

        print("\nGenerated SQL:")
        print("-" * 60)
        print(generated_sql)
        print("-" * 60)

        result = execute_sql(generated_sql, DB_PATH)

        print("\nQuery result:")
        print("-" * 60)
        print(result)
        print("-" * 60)

    except Exception as error:
        print(f"\nError: {error}")


if __name__ == "__main__":
    main()