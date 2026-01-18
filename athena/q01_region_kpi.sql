SELECT
  region,
  COUNT(*) AS aircraft_total,
  SUM(CASE WHEN on_ground THEN 1 ELSE 0 END) AS on_ground,
  ROUND(AVG(CASE WHEN on_ground = false THEN velocity END), 2) AS avg_velocity_ms_in_air,
  ROUND(SUM(CASE WHEN dq_ok THEN 1 ELSE 0 END) * 1.0 / COUNT(*), 4) AS dq_ok_rate
FROM flightops.v_silver_states_region
GROUP BY region
ORDER BY aircraft_total DESC;
