# SQL cleaning
# read-only SQL validation

import re


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


def validate_read_only_sql(sql: str) -> None:
    """Validate that the SQL contains one read-only query."""

    if not sql:
        raise ValueError(
            "The generated SQL is empty."
        )

    normalized_sql = re.sub(
        r"\s+",
        " ",
        sql.strip(),
    ).lower()

    if not normalized_sql.startswith(
        ("select ", "with ")
    ):
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

    sql_without_final_semicolon = (
        sql.rstrip().removesuffix(";")
    )

    if ";" in sql_without_final_semicolon:
        raise ValueError(
            "Multiple SQL statements are not allowed."
        )