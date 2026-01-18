SELECT origin_country, region, COUNT(*) AS aircraft
FROM flightops.v_silver_states_region
GROUP BY origin_country, region
ORDER BY aircraft DESC
LIMIT 15;
