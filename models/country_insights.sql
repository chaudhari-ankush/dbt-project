{{ config(
    materialized='table',
    pre_hook="DROP VIEW IF EXISTS {{ this.schema }}.{{ this.identifier }}"
) }}

SELECT
  country,
  COUNT(*) AS customer_count,
  AVG(age) AS avg_age,
  SUM(total_spent) AS total_revenue
FROM {{ source('my_database', 'customers') }}
GROUP BY country
