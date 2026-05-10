# Prompts

## Narrate story, 11 May 2026

<!--

cd /home/sanand/code/publisher-impact-factor
dev.sh
claude --dangerously-skip-permissions --effort medium

-->

Write a narrative story for each of these publishers - Elsevier, Springer Nature, Wiley, Oxford University Press, PLOS - explaining how to improve their publisher impact factor in neuroscience based on the publication data available in data/openalex_mvp.duckdb as well as the insights from ./insights.md.

You don't need to limit yourself to the insights in ./insights.md. You may delegate analyses to the AI coding agent codex, telling it to use the `data-analysis` skill, via `codex --yolo --model gpt-5.5 exec "prompts"` - it has excellent analysis skills.

Some angles to explore might be:

- who's going to your competition and where?
- what trending topic are you not publishing on and what outdated topics are you still publishing on?
- who are the trending funders and outdated funders in your domain?
- which fading authors are you still publishing and which trending authors are you not publishing?

However, these are naive angles. Plan like an expert. In this context, first think about:

- What patterns would an expert in this field check / recognize that beginners would miss?
- What questions would an expert ask that a beginner would not know to?
- What problems / failures would an expert anticipate that beginners may not be aware of?
- What powerful & relevant mental models would an expert apply in this context?

Plan accordingly.

Generate the output as a single page HTML data story (using the data-story skill) for each of the publishers. The file names should be: reports/neuroscience-{publisher-name, e.g. oup, springer-nature, elsevier, wiley, plos}-2026-05.html

Make sure they use the same design - create and re-use styles in reports/style.css.
Make sure they use a similar structure, but the content should be aimed at maximizing the insights for each publisher, you may structure accordingly. Use a template if that will help.

Use sub-agents as required, token-efficiently.

IMPORTANT: Because Claude will almost certainly stall when generating such a large file at one shot, break this into parts, generating the .html in chunks or layered edits (keeping each chunk small, max 100KB of edits) and saving it, checking it, then updating it with the next iteration, and so on.


## Download OpenAlex data, 07 May 2026

<!--

cd /home/sanand/code/publisher-impact-factor
dev.sh
codex

-->

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

<!-- codex resume 019e00ff-aef2-7eb2-820c-75c490bf3cad -->
