# 각 질문을 순회하며 SQL문 생성

from src.llm import generate_sql
from src.prompt import build_prompt
from src.validator import (
    clean_sql,
    validate_read_only_sql,
)


def generate_sql_for_questions(
    questions: list[str],
    schema: str,
) -> list[dict[str, str]]:
    """Generate and validate SQL for all test questions."""

    results: list[dict[str, str]] = []

    total_questions = len(questions)

    for index, question in enumerate(
        questions,
        start=1,
    ):
        print("=" * 70)
        print(
            f"Processing question "
            f"{index}/{total_questions}"
        )
        print("=" * 70)

        print(f"\nQuestion:\n{question}")

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

            result = {
                "question": question,
                "generated_sql": generated_sql,
                "status": "success",
                "error_message": "",
            }

            print(
                f"\nGenerated SQL:\n"
                f"{generated_sql}"
            )

            print("\nStatus: success")

        except Exception as error:
            result = {
                "question": question,
                "generated_sql": "",
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

    failed_count = (
        len(results) - success_count
    )

    print("=" * 70)
    print("Batch Generation Summary")
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