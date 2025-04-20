SELECT
  DATE(pacific_time) AS date,
  COUNT(*) AS songs_played
FROM `my-project-id.spotify_data.deduped_plays_pacific`
GROUP BY date
ORDER BY date
