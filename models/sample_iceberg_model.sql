-- Sample Iceberg dbt model
{{ config(materialized='table') }}

SELECT * FROM glue_catalog.sample_db.sample_iceberg_table LIMIT 10 