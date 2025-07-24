-- Sample Iceberg dbt model
{{ config(materialized='table') }}

SELECT * FROM bronze.aa_asset_mgr_supplier  