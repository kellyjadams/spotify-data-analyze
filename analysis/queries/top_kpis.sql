WITH filtered_data AS (
  SELECT *
  FROM `my-project-id.spotify_data.deduped_plays_pacific`
  WHERE pacific_time BETWEEN PARSE_DATE('%Y%m%d', @DS_START_DATE) AND PARSE_DATE('%Y%m%d', @DS_END_DATE)
),

artist_list AS (
  SELECT DISTINCT TRIM(artist) AS artist
  FROM filtered_data,
  UNNEST(SPLIT(artists, ',')) AS artist
  WHERE TRIM(artist) != ''
),

genre_list AS (
  SELECT DISTINCT TRIM(genre_item) AS genre
  FROM filtered_data,
  UNNEST(SPLIT(genre, ',')) AS genre_item
  WHERE TRIM(genre_item) != ''
),

album_list AS (
  SELECT DISTINCT album
  FROM filtered_data
  WHERE album IS NOT NULL AND TRIM(album) != ''
)

SELECT
  (SELECT COUNT(*) FROM filtered_data) AS total_tracks,
  (SELECT COUNT(*) FROM artist_list) AS unique_artists,
  (SELECT COUNT(*) FROM genre_list) AS unique_genres,
  (SELECT COUNT(*) FROM album_list) AS unique_albums,
  ROUND(SUM(duration_ms) / 1000 / 60 / 60, 2) AS listening_hours,
  ROUND(AVG(duration_ms) / 60000, 2) AS avg_track_duration_mins
FROM filtered_data
