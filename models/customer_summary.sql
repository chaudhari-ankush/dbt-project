{{ config(
    materialized='table',
    pre_hook="DROP VIEW IF EXISTS {{ this.schema }}.{{ this.identifier }}"
) }}

SELECT
  customer_segment,
  COUNT(*) AS total_customers,
  AVG(total_spent) AS avg_spent
FROM {{ source('my_database', 'customers') }}
GROUP BY customer_segment
