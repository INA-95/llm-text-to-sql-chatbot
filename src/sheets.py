# Google Spreadsheets 연결
# 질문 읽기
# SQL 출력 결과 입력

import gspread
from google.oauth2.service_account import Credentials

from src.config import (
    CREDENTIALS_PATH,
    GOOGLE_SCOPES,
    QUESTION_COLUMN,
    RESULT_SQL_COLUMN,
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


def get_questions_from_sheet(
    worksheet: gspread.Worksheet,
) -> list[str]:
    """Read non-empty questions from the questions column."""

    records = worksheet.get_all_records()

    questions: list[str] = []

    for record in records:
        question = str(
            record.get(
                QUESTION_COLUMN,
                "",
            )
        ).strip()

        if question:
            questions.append(question)

    return questions


def update_generated_sql(
    worksheet: gspread.Worksheet,
    results: list[dict[str, str]],
) -> None:
    """Write generated SQL into the result_sql column."""

    if not results:
        print(
            "No SQL results are available to update."
        )
        return

    headers = worksheet.row_values(1)

    if RESULT_SQL_COLUMN not in headers:
        raise ValueError(
            f"Column not found: {RESULT_SQL_COLUMN}"
        )

    result_column_index = (
        headers.index(RESULT_SQL_COLUMN) + 1
    )

    result_column_letter = (
        gspread.utils.rowcol_to_a1(
            1,
            result_column_index,
        )[:-1]
    )

    values = [
        [
            result["generated_sql"]
            if result["status"] == "success"
            else ""
        ]
        for result in results
    ]

    start_row = 2
    end_row = start_row + len(values) - 1

    range_name = (
        f"{result_column_letter}{start_row}:"
        f"{result_column_letter}{end_row}"
    )

    worksheet.update(
        range_name=range_name,
        values=values,
    )

    print(
        f"\nUpdated {len(values)} SQL results "
        f"in Google Sheets."
    )