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

## Example

### Input (Google Sheets)

| Question | Human SQL |
|----------|-----------|
| How many users were recorded in total? | SELECT ... |

### Console Output

```text
Processing Question 1/1...

✓ LLM SQL generated
✓ LLM SQL executed successfully
✓ Human SQL executed successfully

Updated 1 evaluation result in Google Sheets.
```

### Output (Google Sheets)

| question | llm_sql | llm_sql_result | human_sql | human_sql_result |
|----------|---------|----------------|-----------|------------------|
| Which traffic source generated the highest donation conversion rate? | SELECT ... | source_medium: youtube / video<br>conversion_rate: 0.99% | SELECT ... | source_medium: youtube / video<br>conversion_rate: 0.99% |
