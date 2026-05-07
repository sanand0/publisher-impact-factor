# Prompts

<!--

cd /home/sanand/code/publisher-impact-factor
dev.sh
codex

-->

## Download OpenAlex data, 07 Mar 2026

<!-- Metaprompt: https://chatgpt.com/c/69fc23ad-b9c8-83ea-a6eb-13ced1a7c281 -->

Create an agent-friendly CLI `download_openalex.py` that downloads data from the OpenAlex API for an "Impact Factor Improvement Report" demo.

It accepts:

- target domain/topic query, e.g. "neuroscience"
- start date, default 2020-01-01
- end date, default today
- a list of publisher names, e.g. Elsevier, Springer Nature, Wiley, Oxford University Press, PLOS
- optional target journal ISSN or journal name

Restartably download and cache enough OpenAlex data to analyze:

1. competing journals/sources in the domain
2. works/articles by journal and publisher
3. article abstracts and metadata
4. authors and institutions
5. topics/subfields
6. citations / cited_by_count
7. open-access status
8. funder/grant metadata where available
9. retraction flag where available

Use only the OpenAlex API, not the full snapshot.

Important OpenAlex constraints:

- Use cursor pagination for bounded queries only.
- Do not try to download all OpenAlex works.
- Respect rate limits with retries/backoff.
- Add a `mailto=` parameter to all OpenAlex requests. Make it configurable via `--email`.

Implementation requirements:

- Use `requests`, `pandas`, `pyarrow`, `duckdb`, `tqdm`, and standard library only.
- Save raw JSONL files and normalized Parquet files.
- Maintain a small DuckDB database for easy querying.
- Cache responses and re-use cached files on subsequent runs unless `--refresh` is set.
- Use an output directory structure like:
  - data/raw/{publishers,sources,works}.jsonl
  - data/parquet/{publishers,sources,works,authorships,institutions,work_topics,work_funders}.parquet
  - data/openalex_mvp.duckdb

CLI arguments:

- `--domain-query`, default "neuroscience"
- `--publishers`, comma-separated, default "Elsevier,Springer Nature,Wiley,Oxford University Press,PLOS"
- `--start-date`, default "2020-01-01"
- `--end-date`, default today
- `--email`, required
- `--max-works-per-publisher`, default 5000
- `--max-sources-per-publisher`, default 50
- `--out-dir`, default "data"
- `--refresh`, if set, re-download instead of using cached files

Workflow:

1. Search OpenAlex publishers by name and save matched publisher records.
2. For each publisher, fetch journal sources using filters/search where possible.
3. Find domain-relevant sources by checking source names, source topics/fields/subfields where available, and works returned by `title_and_abstract.search`.
4. For each selected source/journal, download works from the date range with filters:
   - publication date range
   - type: article OR review where possible
   - source/journal ID
   - title/abstract domain search where useful
5. Extract and normalize:
   - works: id, doi, title, publication_date, publication_year, type, cited_by_count, is_retracted, open_access fields, primary source id/name/issn/publisher, abstract text reconstructed from `abstract_inverted_index`
   - authorships: work_id, author_id, author_name, author_position, corresponding flag if available
   - institutions: work_id, author_id, institution_id, institution_name, country_code, ror, type
   - topics: work_id, topic_id, topic_name, subfield, field, domain, score if available
   - funders/grants: work_id, funder_id, funder_name, award_id if available
6. Save raw JSONL and Parquet.
7. Create DuckDB tables over the Parquet files.
8. Show progress. Print summary stats at the end.

Run and test the script for a sample (email: root.node@gmail.com, topic: neuroscience, use publisher names mentioned above) to ensure it works as expected, handles errors gracefully, and respects rate limits.

Document usage in README.md, with examples, mentioning what the script downloads and does not download.

Commit as you go (including .gitignore and prompts.md, which I'm editing).

---

What command downloads all papers in the neuroscience topic for publishers: Elsevier, Springer Nature, Wiley, Oxford University Press, PLOS?
