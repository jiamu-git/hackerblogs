import duckdb, time
con = duckdb.connect(); con.execute("SET threads=4")
t0=time.time()
con.execute("""
COPY (
  SELECT regexp_extract(url,'^https?://([^/]+)',1) AS host,
         url, score, CAST(date_trunc('year', time) AS DATE) AS yr, title
  FROM read_parquet('hacker-news/data/*/*.parquet')
  WHERE type=1 AND url IS NOT NULL AND url <> ''
) TO 'blogs/story_urls.parquet' (FORMAT PARQUET, COMPRESSION ZSTD)
""")
print("story urls:", con.execute("SELECT count(*), count(DISTINCT host) FROM 'blogs/story_urls.parquet'").fetchone(), f"{time.time()-t0:.0f}s")
con.execute("""
COPY (
  SELECT lower(regexp_replace(host,'^www\\.','')) AS d,
         count(DISTINCT url) AS urls,
         count(*) FILTER (WHERE yr >= DATE '2023-01-01') AS recent_posts,
         count(DISTINCT yr) AS yrs
  FROM 'blogs/story_urls.parquet'
  GROUP BY 1
) TO 'blogs/domain_urls.parquet' (FORMAT PARQUET, COMPRESSION ZSTD)
""")
print("ok", f"{time.time()-t0:.0f}s")
