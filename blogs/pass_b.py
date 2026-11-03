"""Pass B (v2): decode HTML-escaped URLs in comments, aggregate per domain/url/year."""
import duckdb, time
con = duckdb.connect()
con.execute("SET threads=4")
con.execute("SET memory_limit='8GB'")
t0 = time.time()

def dec(col):
    return (f"regexp_replace(regexp_replace(regexp_replace({col}, '&#x2F;', '/', 'g'), "
            f"'&#x2F', '/', 'g'), '&amp;', '&', 'g')")

con.execute(f"""
CREATE TABLE links AS
SELECT u, regexp_extract(u, '^https?://([^/]+)', 1) AS host, time
FROM (
  SELECT unnest(regexp_extract_all(
      {dec('text')},
      'https?://[^\\s)"''<>]+')) AS u, time
  FROM read_parquet('hacker-news/data/*/*.parquet')
  WHERE type = 2 AND text LIKE '%http%' AND text IS NOT NULL
) t
""")
print("links:", con.execute("SELECT count(*), count(DISTINCT host) FROM links").fetchone(), f"{time.time()-t0:.0f}s", flush=True)

con.execute("""
COPY (
  SELECT host, u AS url, CAST(date_trunc('year', time) AS DATE) AS yr, count(*) AS n
  FROM links
  WHERE host <> ''
  GROUP BY 1,2,3
) TO 'blogs/comment_links.parquet' (FORMAT PARQUET, COMPRESSION ZSTD)
""")
print("rows:", con.execute("SELECT count(*) FROM 'blogs/comment_links.parquet'").fetchone(), f"{time.time()-t0:.0f}s")
