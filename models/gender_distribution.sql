{{ config(
    materialized='table',
    pre_hook="DROP VIEW IF EXISTS {{ this.schema }}.{{ this.identifier }}"
) }}

SELECT
  gender,
  COUNT(*) AS total_customers,
  AVG(total_spent) AS avg_spent_per_gender
FROM {{ source('my_database', 'customers') }}
GROUP BY gender
