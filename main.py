# 전체 실행 순서만 담당

import gspread

from src.config import DB_PATH
from src.database import get_database_schema
from src.pipeline import (
    generate_sql_for_questions,
    print_summary,
)
from src.sheets import (
    get_questions_from_sheet,
    get_worksheet,
    update_generated_sql,
)


def main() -> None:
    try:
        print(
            "Extracting database schema..."
        )

        schema = get_database_schema(
            DB_PATH
        )

        print(
            "Connecting to Google Sheets..."
        )

        worksheet = get_worksheet()

        questions = get_questions_from_sheet(
            worksheet
        )

        if not questions:
            print(
                "No questions were found in "
                "the 'questions' column."
            )
            return

        print(
            f"Loaded {len(questions)} questions "
            "from Google Sheets.\n"
        )

        results = generate_sql_for_questions(
            questions=questions,
            schema=schema,
        )

        update_generated_sql(
            worksheet=worksheet,
            results=results,
        )

        print_summary(results)

    except FileNotFoundError as error:
        print(f"\nFile error: {error}")

    except gspread.SpreadsheetNotFound:
        print(
            "\nSpreadsheet not found, or the "
            "service account does not have access."
        )

    except gspread.WorksheetNotFound:
        print(
            "\nWorksheet was not found. "
            "Check WORKSHEET_NAME in config.py."
        )

    except Exception as error:
        print(
            f"\nUnexpected error: "
            f"{type(error).__name__}: {error}"
        )


if __name__ == "__main__":
    main()