# Google Spreadsheets 연결
# 질문 및 Human SQL 읽기
# LLM SQL과 실행 결과 입력

import gspread
from google.oauth2.service_account import Credentials

from src.config import (
    CREDENTIALS_PATH,
    GOOGLE_SCOPES,
    HUMAN_SQL_COLUMN,
    HUMAN_SQL_RESULT_COLUMN,
    LLM_SQL_COLUMN,
    LLM_SQL_RESULT_COLUMN,
    QUESTION_COLUMN,
    SPREADSHEET_ID,
    WORKSHEET_NAME,
)


def get_worksheet() -> gspread.Worksheet:
    """Authenticate and return the target Google worksheet."""

    if not CREDENTIALS_PATH.exists():
        raise FileNotFoundError(
            "Google credentials file not found: "
            f"{CREDENTIALS_PATH.resolve()}"
        )

    credentials = (
        Credentials.from_service_account_file(
            CREDENTIALS_PATH,
            scopes=GOOGLE_SCOPES,
        )
    )

    client = gspread.authorize(
        credentials
    )

    spreadsheet = client.open_by_key(
        SPREADSHEET_ID
    )

    return spreadsheet.worksheet(
        WORKSHEET_NAME
    )


def get_test_cases_from_sheet(
    worksheet: gspread.Worksheet,
) -> list[dict[str, str]]:
    """Read questions and human-written SQL from Google Sheets."""

    records = worksheet.get_all_records()

    test_cases: list[dict[str, str]] = []

    for record in records:
        question = str(
            record.get(
                QUESTION_COLUMN,
                "",
            )
        ).strip()

        human_sql = str(
            record.get(
                HUMAN_SQL_COLUMN,
                "",
            )
        ).strip()

        if not question:
            continue

        test_cases.append(
            {
                "question": question,
                "human_sql": human_sql,
            }
        )

    return test_cases


def update_evaluation_results(
    worksheet: gspread.Worksheet,
    results: list[dict[str, str]],
) -> None:
    """Write LLM SQL and SQL execution results to Google Sheets."""

    if not results:
        print(
            "No evaluation results are available to update."
        )
        return

    headers = worksheet.row_values(1)

    required_columns = [
        LLM_SQL_COLUMN,
        LLM_SQL_RESULT_COLUMN,
        HUMAN_SQL_RESULT_COLUMN,
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in headers
    ]

    if missing_columns:
        raise ValueError(
            "Columns not found: "
            + ", ".join(missing_columns)
        )

    llm_sql_column_index = (
        headers.index(LLM_SQL_COLUMN) + 1
    )

    llm_result_column_index = (
        headers.index(LLM_SQL_RESULT_COLUMN) + 1
    )

    human_result_column_index = (
        headers.index(HUMAN_SQL_RESULT_COLUMN) + 1
    )

    start_row = 2
    end_row = start_row + len(results) - 1

    llm_sql_values = [
        [result["llm_sql"]]
        for result in results
    ]

    llm_result_values = [
        [result["llm_sql_result"]]
        for result in results
    ]

    human_result_values = [
        [result["human_sql_result"]]
        for result in results
    ]

    worksheet.update(
        range_name=(
            f"{gspread.utils.rowcol_to_a1(start_row, llm_sql_column_index)}:"
            f"{gspread.utils.rowcol_to_a1(end_row, llm_sql_column_index)}"
        ),
        values=llm_sql_values,
    )

    worksheet.update(
        range_name=(
            f"{gspread.utils.rowcol_to_a1(start_row, llm_result_column_index)}:"
            f"{gspread.utils.rowcol_to_a1(end_row, llm_result_column_index)}"
        ),
        values=llm_result_values,
    )

    worksheet.update(
        range_name=(
            f"{gspread.utils.rowcol_to_a1(start_row, human_result_column_index)}:"
            f"{gspread.utils.rowcol_to_a1(end_row, human_result_column_index)}"
        ),
        values=human_result_values,
    )

    print(
        f"\nUpdated {len(results)} evaluation results "
        f"in Google Sheets."
    )