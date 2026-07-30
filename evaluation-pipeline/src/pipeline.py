# 각 질문을 순회하며 LLM SQL과 Human SQL 생성·실행

from src.config import DB_PATH
from src.database import execute_sql
from src.llm import generate_sql
from src.prompt import build_prompt
from src.validator import (
    clean_sql,
    validate_read_only_sql,
)


def format_sql_result(
    columns: list[str],
    rows: list[tuple],
) -> str:
    """Format SQL execution results for Google Sheets."""

    if not rows:
        return "No rows returned"

    formatted_lines = [
        " | ".join(columns)
    ]

    for row in rows:
        formatted_row = " | ".join(
            "" if value is None else str(value)
            for value in row
        )

        formatted_lines.append(
            formatted_row
        )

    return "\n".join(formatted_lines)


def generate_sql_for_questions(
    test_cases: list[dict[str, str]],
    schema: str,
) -> list[dict[str, str]]:
    """Generate LLM SQL and execute both LLM and human-written SQL."""

    results: list[dict[str, str]] = []

    total_questions = len(test_cases)

    for index, test_case in enumerate(
        test_cases,
        start=1,
    ):
        question = test_case["question"]
        human_sql = test_case["human_sql"]

        print("=" * 70)
        print(
            f"Processing question "
            f"{index}/{total_questions}"
        )
        print("=" * 70)

        print(f"\nQuestion:\n{question}")

        generated_sql = ""
        llm_sql_result = ""
        human_sql_result = ""

        try:
            prompt = build_prompt(
                question=question,
                schema=schema,
            )

            raw_sql = generate_sql(prompt)
            generated_sql = clean_sql(raw_sql)

            validate_read_only_sql(
                generated_sql
            )

            llm_columns, llm_rows = execute_sql(
                sql=generated_sql,
                db_path=DB_PATH,
            )

            llm_sql_result = format_sql_result(
                columns=llm_columns,
                rows=llm_rows,
            )

            if human_sql:
                validate_read_only_sql(
                    human_sql
                )

                human_columns, human_rows = execute_sql(
                    sql=human_sql,
                    db_path=DB_PATH,
                )

                human_sql_result = format_sql_result(
                    columns=human_columns,
                    rows=human_rows,
                )

            result = {
                "question": question,
                "llm_sql": generated_sql,
                "llm_sql_result": llm_sql_result,
                "human_sql": human_sql,
                "human_sql_result": human_sql_result,
                "status": "success",
                "error_message": "",
            }

            print(
                f"\nGenerated SQL:\n"
                f"{generated_sql}"
            )

            print(
                f"\nLLM SQL Result:\n"
                f"{llm_sql_result}"
            )

            print(
                f"\nHuman SQL Result:\n"
                f"{human_sql_result}"
            )

            print("\nStatus: success")

        except Exception as error:
            result = {
                "question": question,
                "llm_sql": generated_sql,
                "llm_sql_result": llm_sql_result,
                "human_sql": human_sql,
                "human_sql_result": human_sql_result,
                "status": "failed",
                "error_message": str(error),
            }

            print("\nStatus: failed")
            print(f"Error: {error}")

        results.append(result)

        print()

    return results

def print_summary(
    results: list[dict[str, str]],
) -> None:
    """Print a batch-processing summary."""

    success_count = sum(
        result["status"] == "success"
        for result in results
    )

    failed_count = len(results) - success_count

    print("=" * 70)
    print("Batch Processing Summary")
    print("=" * 70)
    print(
        f"Total questions: {len(results)}"
    )
    print(
        f"Successful: {success_count}"
    )
    print(
        f"Failed: {failed_count}"
    )

    if failed_count:
        print("\nFailed questions:")

        for result in results:
            if result["status"] == "failed":
                print(
                    f"- {result['question']}: "
                    f"{result['error_message']}"
                )