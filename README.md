# Insurance Data Pipeline Project

## Overview
End-to-end data pipeline using Python.

## Flow
Ingestion → Standardization → Validation → Transformation → CDC → Warehouse

## Features
- Multi-source ingestion (CSV, API, DB)
- Data validation
- Transformation and aggregation
- CDC (INSERT, UPDATE, DELETE)
- Incremental load
- Warehouse upsert

## Tech Stack
Python, Pandas, SQLAlchemy, SQLite

## Run
python pipeline/run_pipeline.py