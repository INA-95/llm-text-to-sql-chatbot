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
WORKSHEET_NAME = "Sheet3"

QUESTION_COLUMN = "questions"
HUMAN_SQL_COLUMN = "human_sql"

LLM_SQL_COLUMN = "llm_sql"
LLM_SQL_RESULT_COLUMN = "llm_sql_result"

HUMAN_SQL_RESULT_COLUMN = "human_sql_result"


# Google Sheets API scope
GOOGLE_SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
]