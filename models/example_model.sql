-- Example model that creates a simple aggregation
WITH source_data AS (
    SELECT 
        date_trunc('day', current_timestamp) as date,
        'sample_data' as source,
        generate_series(1, 10) as value
)

SELECT 
    date,
    source,
    COUNT(*) as count,
    AVG(value) as avg_value,
    MIN(value) as min_value,
    MAX(value) as max_value
FROM source_data
GROUP BY date, source 