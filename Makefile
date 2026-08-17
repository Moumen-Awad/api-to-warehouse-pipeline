.PHONY: up down extract load transform test all

include .env
export

up:
	docker compose up -d

down:
	docker compose down

extract:
	python airflow/include/src/extract.py

load:
	python airflow/include/src/load.py

transform:
	cd airflow/include/warehouse_dbt && dbt run

test:
	cd airflow/include/warehouse_dbt && dbt test

all: up extract load transform test
