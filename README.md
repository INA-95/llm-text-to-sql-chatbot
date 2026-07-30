## End-to-End Evaluation Workflow

```text
Google Sheets
──────────────────────────────────────────────
Question
Human SQL
        │
        ▼
Generate SQL using LLM
        │
        ▼
Execute LLM SQL
        │
        ▼
Execute Human SQL
        │
        ▼
Write results back to Google Sheets
──────────────────────────────────────────────
LLM SQL
LLM SQL Result
Human SQL Result
```

The current pipeline automatically:

1. Reads user questions and human-written SQL from Google Sheets.
2. Generates SQL using an LLM.
3. Executes the generated SQL against the evaluation database.
4. Executes the corresponding human-written SQL.
5. Writes the generated SQL and both execution results back to Google Sheets for manual evaluation.
