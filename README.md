# API-to-Warehouse Pipeline

An end-to-end data engineering pipeline built to practice real-world ELT design. It extracts daily cryptocurrency market data from the free CoinGecko REST API, loads raw JSON into a local PostgreSQL warehouse, and transforms it into analytics-ready models using dbt. The entire workflow is fully containerized with Docker and automated using Apache Airflow.

## Demo

![Pipeline running successfully](docs/assets/demo.gif)

## Simple Architecture

![Architecture Diagram](docs/assets/architecture.png)

## Data Dictionary

The data exists after the transformation in the mart table: [Data Dictionary](docs/data_dictionary.md).