SELECT
  EXTRACT(DAYOFWEEK FROM pacific_time) AS weekday_num,  -- 1 = Sunday, 7 = Saturday
  FORMAT_DATE('%A', DATE(pacific_time)) AS weekday_name,
  EXTRACT(HOUR FROM pacific_time) AS hour,
  ROUND(SUM(duration_ms) / 1000 / 60, 1) AS total_minutes
FROM `my-project-id.spotify_data.deduped_plays_pacific`
WHERE 
  pacific_time BETWEEN PARSE_DATE('%Y%m%d', @DS_START_DATE) AND PARSE_DATE('%Y%m%d', @DS_END_DATE)
GROUP BY 
  weekday_num, 
  weekday_name, 
  hour
