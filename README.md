# Text-to-SQL Evaluation Framework

## Overview

This project demonstrates an end-to-end Text-to-SQL pipeline using SQLite and OpenAI.

## Pipeline

```mermaid
flowchart TD
    A[Natural Language Question]
    B[Schema Extraction]
    C[Prompt Generation]
    D[OpenAI API]
    E[SQL Generation]
    F[SQL Validation]
    G[SQLite Execution]
    H[Query Result]

    A --> B --> C --> D --> E --> F --> G --> H

## Tech Stack

- Python
- SQLite
- OpenAI API
