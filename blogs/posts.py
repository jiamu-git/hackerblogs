"""Blog post canon: URLs repeatedly submitted / mentioned across years."""
import duckdb
con = duckdb.connect(); con.execute("SET threads=4")

NORM = """regexp_replace(regexp_replace(regexp_replace(regexp_replace(lower(url),
        '^https?://(www\\.)?', ''), '#.*$', ''), '/+$', ''), '\\?(utm_[^&]*&?|ref=.*)$', '')"""

con.execute(f"""
CREATE TABLE stories AS
SELECT {NORM} AS key, any_value(url) AS url, any_value(host) AS host,
       count(DISTINCT yr) AS sub_years, count(*) AS sub_n,
       max(score) AS best_score, any_value(title) AS title
FROM 'blogs/story_urls.parquet' GROUP BY 1
""")
con.execute(f"""
CREATE TABLE comments AS
SELECT {NORM} AS key, any_value(host) AS host, any_value(url) AS url2, sum(n) AS cmt_n, count(DISTINCT yr) AS cmt_years
FROM 'blogs/comment_links.parquet' GROUP BY 1
""")
print(con.execute("SELECT count(*) FROM stories").fetchone(),
      con.execute("SELECT count(*) FROM comments").fetchone())

con.execute("""
COPY (
  SELECT COALESCE(s.key, c.key) AS key,
         COALESCE(s.url, c.url2) AS url, COALESCE(s.host, c.host) AS host, s.title,
         COALESCE(s.sub_years,0) AS sub_years, COALESCE(s.sub_n,0) AS sub_n,
         COALESCE(s.best_score,0) AS best_score,
         COALESCE(c.cmt_n,0) AS cmt_n, COALESCE(c.cmt_years,0) AS cmt_years,
         GREATEST(COALESCE(s.sub_years,0), COALESCE(c.cmt_years,0)) AS years
  FROM stories s FULL OUTER JOIN comments c ON s.key = c.key
  WHERE GREATEST(COALESCE(s.sub_years,0), COALESCE(c.cmt_years,0)) >= 2
) TO 'blogs/post_canon.parquet' (FORMAT PARQUET, COMPRESSION ZSTD)
""")
n = con.execute("SELECT count(*) FROM 'blogs/post_canon.parquet'").fetchone()[0]
print("multi-year posts:", n)
print(con.execute("""SELECT host, count(*) c, max(cmt_n) mx FROM 'blogs/post_canon.parquet'
                     GROUP BY 1 ORDER BY c DESC LIMIT 12""").fetchall())
