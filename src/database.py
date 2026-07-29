# SQLite schema 추출
# SQL 실행


import sqlite3
from pathlib import Path


def get_database_schema(db_path: Path) -> str:
    """Extract table and column information from a SQLite database."""

    if not db_path.exists():
        raise FileNotFoundError(
            f"Database not found: {db_path.resolve()}"
        )

    schema_lines: list[str] = []

    with sqlite3.connect(db_path) as connection:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
              AND name NOT LIKE 'sqlite_%'
            ORDER BY name;
            """
        )

        table_names = [
            row[0]
            for row in cursor.fetchall()
        ]

        if not table_names:
            raise ValueError(
                "No user-created tables were found in the database."
            )

        for table_name in table_names:
            schema_lines.append(
                f"Table: {table_name}"
            )

            cursor.execute(
                f'PRAGMA table_info("{table_name}");'
            )

            columns = cursor.fetchall()

            for column in columns:
                column_name = column[1]
                column_type = column[2] or "UNKNOWN"

                schema_lines.append(
                    f"- {column_name}: {column_type}"
                )

            schema_lines.append("")

    return "\n".join(schema_lines).strip()


def execute_sql(
    sql: str,
    db_path: Path,
) -> tuple[list[str], list[tuple]]:
    """Execute a read-only SQL query on SQLite."""

    database_uri = (
        f"file:{db_path.resolve()}?mode=ro"
    )

    with sqlite3.connect(
        database_uri,
        uri=True,
    ) as connection:
        cursor = connection.cursor()
        cursor.execute(sql)

        rows = cursor.fetchall()

        columns = (
            [
                description[0]
                for description in cursor.description
            ]
            if cursor.description
            else []
        )

    return columns, rows