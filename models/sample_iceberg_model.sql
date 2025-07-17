-- Sample Iceberg dbt model
{{ config(materialized='table') }}

SELECT * FROM glue_catalog.bronze.aa_asset_mgr_supplier LIMIT 10 