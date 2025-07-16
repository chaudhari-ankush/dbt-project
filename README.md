# Spark Iceberg FastAPI Project

This project integrates FastAPI, dbt-core, dbt-spark, Spark Thrift Server, AWS Glue Catalog, and EMR to read Iceberg table data as a dbt model.

## Features
- FastAPI endpoints to trigger dbt runs
- dbt models reading from Iceberg tables via Spark Thrift Server
- AWS Glue Catalog as the metastore
- EMR cluster for Spark execution

## Setup

### 1. Prerequisites
- AWS account with Glue Catalog and S3 bucket
- EMR cluster with Spark, Spark Thrift Server, and Iceberg enabled
- Iceberg table registered in Glue Catalog

### 2. Environment Variables
Set the following environment variables for dbt:
- `SPARK_HOST`: EMR master DNS or Thrift Server host
- `SPARK_PORT`: Thrift Server port (default: 10000)
- `SPARK_USER`: Your username
- `SPARK_SCHEMA`: Target schema/database

### 3. Install Requirements
```bash
pip install -r requirements.txt
```

### 4. Run FastAPI
```bash
uvicorn app.main:app --reload
```

### 5. Trigger dbt Run
Use the `/dbt/run-iceberg` endpoint to run the Iceberg model.

## dbt Model Example
See `models/sample_iceberg_model.sql` for a sample model reading from an Iceberg table.

## Notes
- Update `profiles.yml` and the dbt model with your actual Glue Catalog, S3 bucket, and Iceberg table names.
- Ensure network access from FastAPI/dbt to Spark Thrift Server. 