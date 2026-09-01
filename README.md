# Fanfinder: LLM Text-to-SQL Analytics Chatbot
**A conversational analytics system that enables non-technical users to query business data using natural language.**

This project presents a conversational analytics chatbot that uses LLMs to convert natural-language questions into SQL queries and generate real-time insights. The system is designed for nonprofit organizations that need analytics capabilities but lack SQL expertise.

---

## Project Report
- [Download PDF](./LLM%20Chatbot%20Side%20Project.pdf)

---

## Project Overview

- **Tech Stack:** GPT-4o mini, LangChain, Text-to-SQL pipeline, Google BigQuery  
- **Duration:** Oct 2024 – Mar 2025  
- **Performance Metrics:**  
  - 90% SQL syntax accuracy across 50+ test cases  
  - 90% query accuracy

The system automates:
1. Intent classification  
2. Table selection  
3. SQL generation  
4. Query execution  
5. Answer generation  
6. Insight formatting  

---

## Problem Statement

Nonprofits often possess rich datasets but lack the technical expertise to extract insights.  
This project solves that gap with:

- A **conversational interface**  
- Automated **Text-to-SQL** transformation  
- Error-resilient query generation  
- Domain-aware table classification  

---

## System Architecture

![System Architecture](Architecture.png)

The pipeline consists of six modular components:

### 1. Intent Classification Prompt  
- Validates user questions  
- Detects missing elements  
- Filters irrelevant or abusive queries  

### 2. Table Classification Prompt  
- Determines the appropriate table using schema + pattern matching  
- Prevents mismatches during SQL generation  

### 3. Text-to-SQL Prompt  
- Uses a dual prompt (system + user)  
- Produces consistent SQL output  
- Enforces strict SQL formatting  

### 4. Answer Generation Prompt  
- Converts SQL output into clear, actionable insights  
- Suggests follow-up analytical questions  

### 5. Execution Engine  
- Runs SQL queries on BigQuery  
- Retrieves datasets efficiently  

### 6. Response Layer  
- Converts raw data into summaries, KPIs, and narratives  

---

## QA Automation

To evaluate Text-to-SQL performance during prompt development, I built a separate QA workflow for testing generated SQL and identifying failure patterns.
- Built an automated QA pipeline using **Google Sheets API + OpenAI API**  
- Ran large-scale regression tests  
- Classified failure cases by type:
  - Temporal reasoning  
  - Null value interpretation  
  - Metric calculations  
  - Table mismatch  
  - Excessive or missing SQL constraints  

The automated QA workflow is implemented in the following evaluation pipeline:

📁 **Evaluation Pipeline:** [`evaluation-pipeline/`](./evaluation-pipeline)

## Error-Driven Prompt Refinement

| Error Type |
|---|
|Temporal Reasoning Error|
|Null Value|
|Over-generated Response|
|Restriction|
|Metric Calculation|
|Table selection|


Based on the failure analysis, I iteratively refined the prompts
using error-specific instructions and few-shot examples.

These refinements reduced the overall error rate by 20%.
However, the evaluation focused on aggregate performance.
I did not separately measure which prompting strategy was most
effective for each type of reasoning error.

---

## Final Result

A user can ask:

> “Which campaign gained the most visitors last month?”

The chatbot will:
1. Interpret intent  
2. Select relevant tables  
3. Generate SQL  
4. Execute the query  
5. Present insights  
6. Suggest meaningful follow-up questions  

This creates a fully automated **conversational analytics** workflow.

---

## Reflection

Through this project, key lessons learned include:
- Importance of structured prompt design  
- Balancing model freedom and constraint  
- Understanding LLM limitations (especially reasoning consistency)  
- Value of version tracking in iterative model design  
- Future research question : Do different types of reasoning failures requires different prompting strategies?
---

## Keywords  
`LLM`, `Text-to-SQL`, `LangChain`, `BigQuery`, `Prompt engineering`, `Conversational analytics`, `Nonprofit data`
