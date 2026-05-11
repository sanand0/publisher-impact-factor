# Publisher Impact Intelligence

**[→ View the reports](https://sanand0.github.io/publisher-impact-factor/)**

Data-driven editorial intelligence reports showing how major publishers can improve their journal impact factor — through topic mix, article format strategy, institutional relationships, and portfolio hygiene.

Each report reverse-engineers the citation economics of a publisher's neuroscience portfolio using open bibliometric data from [OpenAlex](https://openalex.org), benchmarked against four competitors.

## May 2026 · Neuroscience Reports

| Publisher | Key finding | Avg cites/work |
|-----------|-------------|---------------:|
| [Springer Nature](https://sanand0.github.io/publisher-impact-factor/neuroscience-springer-nature-2026-05.html) | Review share dropped 62%→33% in 2025 — the engine powering their #1 rank is slowing | 53.8 |
| [PLOS](https://sanand0.github.io/publisher-impact-factor/neuroscience-plos-2026-05.html) | Only 11 reviews in 512 papers (2%) despite reviews earning 43% more citations | 34.3 |
| [Elsevier](https://sanand0.github.io/publisher-impact-factor/neuroscience-elsevier-2026-05.html) | Three drag journals pull the average from 30.3 to 24.3 — The Lancet's power is hidden | 24.3 |
| [Oxford University Press](https://sanand0.github.io/publisher-impact-factor/neuroscience-oup-2026-05.html) | Brain journal (51.3 avg) is buried by 69 Neuro-Oncology conference abstracts at 0.3 avg | 17.5 |
| [Wiley](https://sanand0.github.io/publisher-impact-factor/neuroscience-wiley-2026-05.html) | 85% dementia market share at 9.2 avg dilutes a portfolio with Annals of Neurology at 57.6 | 17.0 |

## Methodology

Reports analyse open metadata from [OpenAlex](https://openalex.org) — a free, comprehensive index of the world's scholarly literature.

**Citation economics framing:** impact factor is treated as a numerator/denominator problem. We identify which journals, topics, and article types add citations efficiently versus expand the denominator without return.

**Key signals analysed:**
- Citation density by journal, article type (reviews vs. articles), topic, and institution
- Article format mix — the review premium is consistent and large across all publishers
- Topic market share — which high-citation topics each publisher is missing or dominating
- Portfolio drag — off-target or low-yield sources that dilute the publisher average
- Year-over-year trajectory — what changed in 2025 that represents a risk or opportunity

**Data:** OpenAlex API, works 2020–2026, filtered to neuroscience domain by publisher. ~2,600 works across 5 publishers. Citation counts as of May 2026.

**Caveat:** These reports use a citation-density proxy for impact factor, not the formally certified JIF from Clarivate. Early-year papers have naturally lower counts due to citation lag.

---

## Data Pipeline

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
