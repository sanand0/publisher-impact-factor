## Publisher Impact Factor Demo Data

`download_openalex.py` downloads a bounded OpenAlex API dataset for an Impact Factor Improvement Report demo. It uses the public API only, not the full OpenAlex snapshot.

```bash
uv run download_openalex.py \
  --email root.node@gmail.com \
  --domain-query neuroscience \
  --publishers "Elsevier,Springer Nature,Wiley,Oxford University Press,PLOS" \
  --start-date 2015-01-01 \
  --end-date 2026-05-07 \
  --max-sources-per-publisher 200 \
  --max-works-per-publisher 20000 \
  --out-dir data
```

Use a smaller smoke-test run while iterating:

```bash
uv run download_openalex.py \
  --email root.node@gmail.com \
  --domain-query neuroscience \
  --max-sources-per-publisher 3 \
  --max-works-per-publisher 20 \
  --out-dir data/sample
```

Target a specific journal by ISSN or exact journal name:

```bash
uv run download_openalex.py \
  --email root.node@gmail.com \
  --domain-query neuroscience \
  --target-journal 1097-6256
```

Machine-readable CLI metadata:

```bash
uv run download_openalex.py --describe
```

## What It Downloads

The script searches OpenAlex publishers by name, samples journal sources for each publisher, keeps domain-relevant sources, and downloads article/review works in the requested publication date range.

`--domain-query` matches papers using journal names, title/abstract search, and topic metadata.

Outputs:

- Raw JSONL: `data/raw/{publishers,sources,works}.jsonl`
- Normalized Parquet: `data/parquet/{publishers,sources,works,authorships,institutions,work_topics,work_funders}.parquet`
- DuckDB database: `data/openalex_mvp.duckdb`

Normalized fields include journal/source metadata, article titles and abstracts, authorships, institutions, topics/subfields, cited-by counts, open-access status, funder/grant metadata where OpenAlex provides it, and the retraction flag.

## What It Does Not Download

The script does not download all OpenAlex works, the full OpenAlex snapshot, PDFs, full text, citation edges, or unbounded source/publisher history. All work queries are bounded by publisher-selected sources, date range, document type, and the domain search query.

## Caching

Existing raw JSONL files are reused on subsequent runs. Pass `--refresh` to re-query OpenAlex and replace cached outputs. Files are written through temporary files and atomically replaced after a successful write.

## Querying

```bash
duckdb data/openalex_mvp.duckdb
```

Example:

```sql
SELECT primary_source_name, COUNT(*) AS works, SUM(cited_by_count) AS citations
FROM works
GROUP BY primary_source_name
ORDER BY citations DESC
LIMIT 20;
```
