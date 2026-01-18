SELECT callsign, origin_country, region, velocity, latitude, longitude
FROM flightops.v_silver_states_region
WHERE on_ground = false
  AND velocity IS NOT NULL
ORDER BY velocity DESC
LIMIT 25;
