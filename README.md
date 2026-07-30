# Fanfinder: LLM-Based Data Analysis Chatbot  
**An Automated Text-to-SQL Analytics System for Nonprofit Organizations**

This project presents a conversational analytics chatbot that uses LLMs to convert natural-language questions into SQL queries and generate real-time insights. The system is designed for nonprofit organizations that need analytics capabilities but lack SQL expertise.

---

## Project Report  
- [Download PDF](./LLM_Chatbot_Side_Project.pdf)

---

## Project Overview

- **Tech Stack:** GPT-4o mini, LangChain, Text-to-SQL pipeline, Google BigQuery  
- **Duration:** Oct 2024 – Mar 2025  
- **Performance Metrics:**  
  - 90% SQL syntax accuracy across 100 test cases  
  - 98% intent alignment accuracy  

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

To evaluate SQL quality and system reliability:
- Built an automated QA pipeline using **Google Sheets API + OpenAI API**  
- Ran large-scale regression tests  
- Classified failure cases by type:
  - Temporal reasoning  
  - Null value interpretation  
  - Metric calculations  
  - Table mismatch  
  - Excessive or missing SQL constraints  

Iterative refinement improved model behavior by **20%**.

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

---

## Keywords  
`LLM`, `Text-to-SQL`, `LangChain`, `BigQuery`, `Prompt engineering`, `Conversational analytics`, `Nonprofit data`
