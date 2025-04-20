SELECT
  DATE(pacific_time) AS date,
  ROUND(SUM(duration_ms) / 1000 / 60, 2) AS listening_minutes
FROM `my-project-id.spotify_data.deduped_plays_pacific`
GROUP BY date
ORDER BY date
