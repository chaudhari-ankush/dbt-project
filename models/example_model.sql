-- Example DBT model
{{ config(
    materialized='table',
    pre_hook="DROP VIEW IF EXISTS {{ this.schema }}.{{ this.identifier }}"
) }}

select * from customers limit 10 

