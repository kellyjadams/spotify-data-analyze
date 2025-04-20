WITH split_genres AS (
  SELECT
    TRIM(genre_item) AS genre,
    duration_ms
  FROM `my-project-id.spotify_data.deduped_plays_pacific`,
  UNNEST(SPLIT(genre, ',')) AS genre_item
  WHERE TRIM(genre_item) != ''
  AND pacific_time BETWEEN PARSE_DATE('%Y%m%d', @DS_START_DATE) AND PARSE_DATE('%Y%m%d', @DS_END_DATE)
)

SELECT
  genre,
  COUNT(*) AS track_count,
  ROUND(SUM(duration_ms) / 1000 / 60, 2) AS total_minutes
FROM split_genres
GROUP BY genre
ORDER BY total_minutes DESC
