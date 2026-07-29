# 경로, 모델명, Spreadsheet ID, Worksheet 이름

from pathlib import Path


# Project root directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent


# SQLite database
DB_PATH = PROJECT_ROOT / "data" / "sample.db"


# Google service account
CREDENTIALS_PATH = (
    PROJECT_ROOT
    / "credentials"
    / "google-service-account.json"
)


# OpenAI
MODEL_NAME = "gpt-5-mini"


# Google Sheets
SPREADSHEET_ID = "1WhdDJocxNrBo111y8FvZ8qyqGxG784pZAATRJPFo1jU"
WORKSHEET_NAME = "Sheet1"

QUESTION_COLUMN = "questions"
RESULT_SQL_COLUMN = "result_sql"


# Google Sheets API scope
GOOGLE_SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
]