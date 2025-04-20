WITH split_artists AS (
  SELECT
    TRIM(artist) AS artist,
    duration_ms
  FROM `my-project-id.spotify_data.deduped_plays_pacific`,
  UNNEST(SPLIT(artists, ',')) AS artist
  WHERE TRIM(artist) != ''
  AND pacific_time BETWEEN PARSE_DATE('%Y%m%d', @DS_START_DATE) AND PARSE_DATE('%Y%m%d', @DS_END_DATE)
)

SELECT
  artist,
  COUNT(*) AS play_count,
  ROUND(SUM(duration_ms) / 1000 / 60, 2) AS total_minutes
FROM split_artists
GROUP BY artist
ORDER BY total_minutes DESC
