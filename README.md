Insurance Data Platform
Overview

I built this project to simulate a real-world insurance data pipeline. It processes data from multiple sources, applies transformations and validations, and loads it into a warehouse using CDC and upsert logic.

This project helped me understand how real data engineering pipelines work end-to-end, including incremental data processing and maintaining data quality.

Architecture

Ingestion → Standardization → Validation → Transformation → CDC → Warehouse → Quality Checks

Tech Stack
Python
Pandas
SQLAlchemy
Parquet
SQLite
Project Structure
ingestion → data ingestion
standardization → data cleaning
validation → data quality checks
transformation → business logic
cdc → change data capture
loading → warehouse loading
pipeline → orchestration
Pipeline Flow
Data Ingestion
Reads data from CSV, APIs, and databases.
Data Standardization
Cleans and formats data and ensures consistency.
Data Validation
Applies data quality checks and business rules.
Data Transformation
Joins policy and claims data and creates curated datasets.
CDC (Change Data Capture)
Identifies insert, update, and delete records.
Warehouse Loading (Upsert)
Deletes existing records and inserts latest records.
Quality Checks
Validates final warehouse data.
How to Run

pip install -r requirements.txt
python pipeline/run_pipeline.py

Author

Harshitha Dantu
Data Engineer

This project was built as a hands-on implementation to strengthen my understanding of data engineering concepts like CDC, pipeline orchestration, and warehouse design.

        +-------------------+
        |   Data Sources    |
        | CSV | API | DB    |
        +---------+---------+
                  |
                  v
        +-------------------+
        |   Ingestion Layer |
        +-------------------+
                  |
                  v
        +-------------------+
        | Standardization   |
        +-------------------+
                  |
                  v
        +-------------------+
        |   Validation      |
        +-------------------+
                  |
                  v
        +-------------------+
        | Transformation    |
        +-------------------+
                  |
                  v
        +-------------------+
        |      CDC          |
        +-------------------+
                  |
                  v
        +-------------------+
        |   Warehouse       |
        | (SQLite DB)       |
        +-------------------+
                  |
                  v
        +-------------------+
        | Quality Checks    |
        +-------------------+