{{ config(
    materialized='table',
    pre_hook="DROP VIEW IF EXISTS {{ this.schema }}.{{ this.identifier }}"
) }}

SELECT *
FROM {{ source('my_database', 'customers') }}
WHERE total_spent > 8000
