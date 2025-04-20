WITH base AS (
  SELECT
    *,
    DATETIME(TIMESTAMP(timestamp), "America/Los_Angeles") AS pacific_time
  FROM `my-project-id.spotify_data.log_songs`
  WHERE EXTRACT(YEAR FROM DATETIME(TIMESTAMP(timestamp), "America/Los_Angeles")) 
        = EXTRACT(YEAR FROM CURRENT_DATETIME("America/Los_Angeles"))
),

numbered AS (
  SELECT
    *,
    LAG(TIMESTAMP(timestamp)) OVER (
      PARTITION BY track, artists 
      ORDER BY TIMESTAMP(timestamp)
    ) AS prev_ts
  FROM base
)

SELECT *
FROM numbered
WHERE 
  prev_ts IS NULL
  OR TIMESTAMP_DIFF(TIMESTAMP(timestamp), prev_ts, MINUTE) >= 5