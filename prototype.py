import re
import sqlite3
from pathlib import Path

from openai import OpenAI


# --------------------------------------------------
# Configuration
# --------------------------------------------------

DB_PATH = Path("data/sample.db")
MODEL_NAME = "gpt-5-mini"

# OPENAI_API_KEY 환경변수를 자동으로 읽음
client = OpenAI()


# --------------------------------------------------
# 1. Extract database schema
# --------------------------------------------------

def get_database_schema(db_path: Path) -> str:
    """Extract table and column information from a SQLite database."""

    schema_lines = []

    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
              AND name NOT LIKE 'sqlite_%'
            ORDER BY name;
            """
        )

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


# --------------------------------------------------
# 2. Build Text-to-SQL prompt
# --------------------------------------------------

def build_prompt(question: str, schema: str) -> str:
    """Create a prompt containing the schema and user question."""

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


# --------------------------------------------------
# 3. Generate SQL with OpenAI
# --------------------------------------------------

def generate_sql(prompt: str) -> str:
    """Send the prompt to OpenAI and return the generated SQL."""

    response = client.responses.create(
        model=MODEL_NAME,
        input=prompt,
    )

    return response.output_text.strip()


# --------------------------------------------------
# 4. Clean generated SQL
# --------------------------------------------------

def clean_sql(raw_sql: str) -> str:
    """Remove Markdown code fences and surrounding whitespace."""

    sql = raw_sql.strip()

    sql = re.sub(
        r"^```(?:sql|sqlite)?\s*",
        "",
        sql,
        flags=re.IGNORECASE,
    )

    sql = re.sub(
        r"\s*```$",
        "",
        sql,
    )

    return sql.strip()


# --------------------------------------------------
# 5. Validate generated SQL
# --------------------------------------------------

def validate_read_only_sql(sql: str) -> None:
    """Allow only one read-only SELECT or WITH query."""

    if not sql:
        raise ValueError("The generated SQL is empty.")

    normalized_sql = re.sub(
        r"\s+",
        " ",
        sql.strip(),
    ).lower()

    if not normalized_sql.startswith(("select ", "with ")):
        raise ValueError(
            "Only SELECT or WITH queries are allowed."
        )

    blocked_keywords = [
        "insert",
        "update",
        "delete",
        "drop",
        "alter",
        "create",
        "replace",
        "attach",
        "detach",
        "vacuum",
        "pragma",
        "reindex",
    ]

    for keyword in blocked_keywords:
        pattern = rf"\b{keyword}\b"

        if re.search(pattern, normalized_sql):
            raise ValueError(
                f"Unsafe SQL keyword detected: {keyword}"
            )

    # 마지막 세미콜론은 허용하지만, 여러 SQL문은 허용하지 않음
    sql_without_final_semicolon = sql.rstrip().removesuffix(";")

    if ";" in sql_without_final_semicolon:
        raise ValueError(
            "Multiple SQL statements are not allowed."
        )


# --------------------------------------------------
# 6. Execute SQL on SQLite
# --------------------------------------------------

def execute_sql(
    sql: str,
    db_path: Path,
) -> tuple[list[str], list[tuple]]:
    """Execute SQL using a read-only SQLite connection."""

    database_uri = f"file:{db_path.resolve()}?mode=ro"

    with sqlite3.connect(
        database_uri,
        uri=True,
    ) as conn:
        cursor = conn.cursor()
        cursor.execute(sql)

        rows = cursor.fetchall()

        if cursor.description is None:
            columns = []
        else:
            columns = [
                description[0]
                for description in cursor.description
            ]

    return columns, rows


# --------------------------------------------------
# 7. Print query result
# --------------------------------------------------

def print_query_result(
    columns: list[str],
    rows: list[tuple],
) -> None:
    """Print query results in a readable format."""

    print("\nQuery Result:")
    print("-" * 60)

    if not columns:
        print("The query did not return any columns.")
        print("-" * 60)
        return

    print(" | ".join(columns))
    print("-" * 60)

    if not rows:
        print("No rows returned.")
    else:
        for row in rows:
            formatted_row = [
                "NULL" if value is None else str(value)
                for value in row
            ]

            print(" | ".join(formatted_row))

    print("-" * 60)


# --------------------------------------------------
# 8. Main pipeline
# --------------------------------------------------

def main() -> None:
    if not DB_PATH.exists():
        print(
            f"Database not found: {DB_PATH.resolve()}"
        )
        return

    try:
        # Schema extraction
        schema = get_database_schema(DB_PATH)

        print("Database Schema:")
        print("-" * 60)
        print(schema)
        print("-" * 60)

        # User question
        question = input(
            "\nAsk a question about the dataset: "
        ).strip()

        if not question:
            raise ValueError(
                "Question cannot be empty."
            )

        # Prompt generation
        prompt = build_prompt(
            question=question,
            schema=schema,
        )

        # OpenAI API call
        print("\nGenerating SQL with OpenAI...")

        raw_sql = generate_sql(prompt)
        generated_sql = clean_sql(raw_sql)

        # SQL validation
        validate_read_only_sql(generated_sql)

        print("\nGenerated SQL:")
        print("-" * 60)
        print(generated_sql)
        print("-" * 60)

        # SQLite execution
        print("\nExecuting SQL on SQLite...")

        columns, rows = execute_sql(
            sql=generated_sql,
            db_path=DB_PATH,
        )

        # Result output
        print_query_result(
            columns=columns,
            rows=rows,
        )

    except ValueError as error:
        print(f"\nValidation error: {error}")

    except sqlite3.Error as error:
        print(f"\nSQLite error: {error}")

    except Exception as error:
        print(
            f"\nUnexpected error: "
            f"{type(error).__name__}: {error}"
        )


if __name__ == "__main__":
    main()