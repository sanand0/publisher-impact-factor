#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "requests",
#   "pandas",
#   "pyarrow",
#   "duckdb",
#   "tqdm",
# ]
# ///
"""Download bounded OpenAlex data for an Impact Factor Improvement demo."""

from __future__ import annotations

import argparse
import json
import os
import random
import re
import sys
import time
from collections.abc import Iterable
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Any

import duckdb
import pandas as pd
import requests
from tqdm import tqdm


API_BASE = "https://api.openalex.org"
DEFAULT_PUBLISHERS = "Elsevier,Springer Nature,Wiley,Oxford University Press,PLOS"
PUBLISHER_ALIASES = {
    "plos": "Public Library of Science",
}
JSONL_NAMES = ("publishers", "sources", "works")
PARQUET_NAMES = (
    "publishers",
    "sources",
    "works",
    "authorships",
    "institutions",
    "work_topics",
    "work_funders",
)


class OpenAlexError(RuntimeError):
    """Raised when OpenAlex cannot satisfy a bounded request."""


@dataclass(frozen=True)
class Config:
    domain_query: str
    publishers: list[str]
    start_date: str
    end_date: str
    email: str
    max_works_per_publisher: int
    max_sources_per_publisher: int
    out_dir: Path
    refresh: bool
    target_journal: str | None
    format: str


class OpenAlexClient:
    def __init__(self, email: str, polite_delay: float = 0.12) -> None:
        self.email = email
        self.polite_delay = polite_delay
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": f"publisher-impact-factor-demo/0.1 (mailto:{email})",
                "Accept": "application/json",
            }
        )

    def get(self, endpoint: str, params: dict[str, Any], *, timeout: int = 60) -> dict[str, Any]:
        query = {key: value for key, value in params.items() if value not in (None, "")}
        query["mailto"] = self.email
        url = f"{API_BASE}/{endpoint.lstrip('/')}"
        last_error: Exception | None = None

        for attempt in range(7):
            try:
                response = self.session.get(url, params=query, timeout=timeout)
                if response.status_code in {429, 500, 502, 503, 504}:
                    retry_after = response.headers.get("retry-after")
                    delay = float(retry_after) if retry_after else min(60, 2**attempt)
                    time.sleep(delay + random.uniform(0, 0.5))
                    continue
                response.raise_for_status()
                time.sleep(self.polite_delay)
                return response.json()
            except (requests.RequestException, ValueError) as error:
                last_error = error
                time.sleep(min(60, 2**attempt) + random.uniform(0, 0.5))

        raise OpenAlexError(f"OpenAlex request failed for {endpoint}: {last_error}")

    def list_cursor(
        self,
        endpoint: str,
        params: dict[str, Any],
        *,
        limit: int,
        desc: str,
    ) -> list[dict[str, Any]]:
        items: list[dict[str, Any]] = []
        cursor = "*"
        per_page = min(200, max(1, limit))
        progress = tqdm(total=limit, desc=desc, unit="rec", leave=False)
        try:
            while len(items) < limit and cursor:
                page = self.get(endpoint, {**params, "per-page": per_page, "cursor": cursor})
                results = page.get("results") or []
                if not results:
                    break
                remaining = limit - len(items)
                items.extend(results[:remaining])
                progress.update(min(len(results), remaining))
                cursor = (page.get("meta") or {}).get("next_cursor")
        finally:
            progress.close()
        return items


def parse_args(argv: list[str] | None = None) -> Config:
    parser = argparse.ArgumentParser(
        description="Download bounded OpenAlex data for an Impact Factor Improvement Report demo."
    )
    parser.add_argument("--domain-query", default="neuroscience")
    parser.add_argument("--publishers", default=DEFAULT_PUBLISHERS)
    parser.add_argument("--start-date", default="2020-01-01")
    parser.add_argument("--end-date", default=date.today().isoformat())
    parser.add_argument("--email", default=os.environ.get("OPENALEX_EMAIL"), required=False)
    parser.add_argument("--max-works-per-publisher", type=int, default=5000)
    parser.add_argument("--max-sources-per-publisher", type=int, default=50)
    parser.add_argument("--out-dir", type=Path, default=Path("data"))
    parser.add_argument("--refresh", action="store_true")
    parser.add_argument("--target-journal", help="Optional target journal ISSN or journal name.")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    parser.add_argument("--describe", action="store_true", help="Print machine-readable CLI metadata.")
    args = parser.parse_args(argv)

    if args.describe:
        print(json.dumps(describe_cli(), indent=2))
        raise SystemExit(0)
    if not args.email:
        parser.error("--email is required, or set OPENALEX_EMAIL")
    for value, arg_name in ((args.start_date, "--start-date"), (args.end_date, "--end-date")):
        try:
            validate_date(value, arg_name)
        except argparse.ArgumentTypeError as error:
            parser.error(str(error))
    if args.start_date > args.end_date:
        parser.error("--start-date must be on or before --end-date")
    if args.max_works_per_publisher < 1:
        parser.error("--max-works-per-publisher must be positive")
    if args.max_sources_per_publisher < 1:
        parser.error("--max-sources-per-publisher must be positive")

    publishers = [part.strip() for part in args.publishers.split(",") if part.strip()]
    if not publishers:
        parser.error("--publishers must contain at least one publisher name")

    return Config(
        domain_query=args.domain_query.strip(),
        publishers=publishers,
        start_date=args.start_date,
        end_date=args.end_date,
        email=args.email.strip(),
        max_works_per_publisher=args.max_works_per_publisher,
        max_sources_per_publisher=args.max_sources_per_publisher,
        out_dir=args.out_dir,
        refresh=args.refresh,
        target_journal=args.target_journal.strip() if args.target_journal else None,
        format=args.format,
    )


def describe_cli() -> dict[str, Any]:
    return {
        "name": "download_openalex.py",
        "description": "Bounded OpenAlex downloader for publisher/journal impact-factor demo analysis.",
        "inputs": {
            "--domain-query": {"type": "string", "default": "neuroscience"},
            "--publishers": {"type": "comma-separated string", "default": DEFAULT_PUBLISHERS},
            "--start-date": {"type": "YYYY-MM-DD", "default": "2020-01-01"},
            "--end-date": {"type": "YYYY-MM-DD", "default": "today"},
            "--email": {"type": "email", "required": True, "env": "OPENALEX_EMAIL"},
            "--max-works-per-publisher": {"type": "integer", "default": 5000},
            "--max-sources-per-publisher": {"type": "integer", "default": 50},
            "--out-dir": {"type": "path", "default": "data"},
            "--target-journal": {"type": "string", "required": False},
            "--refresh": {"type": "boolean", "default": False},
            "--format": {"type": "enum", "values": ["text", "json"], "default": "text"},
        },
        "outputs": {
            "raw_jsonl": [f"data/raw/{name}.jsonl" for name in JSONL_NAMES],
            "parquet": [f"data/parquet/{name}.parquet" for name in PARQUET_NAMES],
            "duckdb": "data/openalex_mvp.duckdb",
        },
    }


def validate_date(value: str, arg_name: str) -> None:
    try:
        datetime.strptime(value, "%Y-%m-%d")
    except ValueError as error:
        raise argparse.ArgumentTypeError(f"{arg_name} must be YYYY-MM-DD") from error


def raw_path(config: Config, name: str) -> Path:
    return config.out_dir / "raw" / f"{name}.jsonl"


def parquet_path(config: Config, name: str) -> Path:
    return config.out_dir / "parquet" / f"{name}.parquet"


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    with path.open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def write_jsonl(path: Path, records: Iterable[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = path.with_suffix(path.suffix + ".tmp")
    with tmp_path.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False, separators=(",", ":")) + "\n")
    tmp_path.replace(path)


def normalize_text(value: str | None) -> str:
    return re.sub(r"[^a-z0-9]+", " ", value.lower()).strip() if value else ""


def openalex_id(value: str | None) -> str | None:
    if not value:
        return None
    return value.rsplit("/", 1)[-1]


def is_issn(value: str) -> bool:
    return bool(re.fullmatch(r"\d{4}-?\d{3}[\dXx]", value.strip()))


def target_matches_source(source: dict[str, Any], target: str | None) -> bool:
    if not target:
        return True
    target_norm = normalize_text(target)
    issn_target = target.replace("-", "").upper()
    if is_issn(target):
        return issn_target in {str(issn).replace("-", "").upper() for issn in source.get("issn") or []}
    names = [source.get("display_name"), *(source.get("alternate_titles") or [])]
    return any(normalize_text(name) == target_norm for name in names if name)


def item_texts(item: dict[str, Any]) -> list[str]:
    texts: list[str] = []
    for key in ("display_name", "display_name_alternatives", "alternate_titles", "abbreviated_title"):
        value = item.get(key)
        if isinstance(value, str):
            texts.append(value)
        elif isinstance(value, list):
            texts.extend(str(part) for part in value if part)
    for topic in item.get("topics") or []:
        texts.append(str(topic.get("display_name") or ""))
        for parent in ("subfield", "field", "domain"):
            nested = topic.get(parent) or {}
            texts.append(str(nested.get("display_name") or ""))
    return texts


def text_matches_domain(item: dict[str, Any], domain_query: str) -> bool:
    needles = set(normalize_text(domain_query).split())
    if not needles:
        return True
    haystack = normalize_text(" ".join(item_texts(item)))
    return any(needle in haystack for needle in needles)


def fetch_publishers(config: Config, client: OpenAlexClient) -> list[dict[str, Any]]:
    cached = raw_path(config, "publishers")
    if cached.exists() and not config.refresh:
        return load_jsonl(cached)

    publishers = []
    for name in tqdm(config.publishers, desc="publishers", unit="publisher"):
        search_name = PUBLISHER_ALIASES.get(normalize_text(name), name)
        page = client.get("publishers", {"search": search_name, "per-page": 10})
        candidates = page.get("results") or []
        if not candidates:
            tqdm.write(f"warning: no OpenAlex publisher match for {name!r}")
            continue
        name_norm = normalize_text(name)
        best = next((item for item in candidates if normalize_text(item.get("display_name")) == name_norm), candidates[0])
        best["_query_name"] = name
        publishers.append(best)

    write_jsonl(cached, publishers)
    return publishers


def source_filter_for_publisher(publisher_id: str) -> str:
    return f"host_organization.id:{publisher_id},type:journal"


def fetch_candidate_sources(
    config: Config, client: OpenAlexClient, publishers: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    cached = raw_path(config, "sources")
    if cached.exists() and not config.refresh:
        return load_jsonl(cached)

    all_sources: list[dict[str, Any]] = []
    seen_ids: set[str] = set()
    for publisher in tqdm(publishers, desc="sources", unit="publisher"):
        publisher_id = openalex_id(publisher.get("id"))
        if not publisher_id:
            continue
        params = {
            "filter": source_filter_for_publisher(publisher_id),
            "sort": "works_count:desc",
        }
        try:
            sources = client.list_cursor(
                "sources",
                params,
                limit=config.max_sources_per_publisher,
                desc=f"sources {publisher.get('display_name', publisher_id)[:24]}",
            )
        except OpenAlexError as error:
            tqdm.write(f"warning: source lookup failed for {publisher.get('display_name')}: {error}")
            sources = []

        for source in sources:
            source_id = source.get("id")
            if source_id and source_id not in seen_ids:
                source["_publisher_id"] = publisher.get("id")
                source["_publisher_name"] = publisher.get("display_name")
                seen_ids.add(source_id)
                all_sources.append(source)

    selected = select_domain_sources(config, client, all_sources)
    write_jsonl(cached, selected)
    return selected


def select_domain_sources(
    config: Config, client: OpenAlexClient, sources: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    selected: list[dict[str, Any]] = []
    progress = tqdm(sources, desc="domain sources", unit="source")
    for source in progress:
        if not target_matches_source(source, config.target_journal):
            continue
        if text_matches_domain(source, config.domain_query):
            source["_domain_match_method"] = "source_metadata"
            selected.append(source)
            continue
        source_id = openalex_id(source.get("id"))
        if not source_id:
            continue
        probe_filter = ",".join(
            [
                f"from_publication_date:{config.start_date}",
                f"to_publication_date:{config.end_date}",
                "type:article|review",
                f"primary_location.source.id:{source_id}",
                f"title_and_abstract.search:{config.domain_query}",
            ]
        )
        try:
            page = client.get("works", {"filter": probe_filter, "per-page": 1})
        except OpenAlexError as error:
            tqdm.write(f"warning: source probe failed for {source.get('display_name')}: {error}")
            continue
        count = ((page.get("meta") or {}).get("count")) or len(page.get("results") or [])
        if count:
            source["_domain_match_method"] = "domain_work_probe"
            source["_domain_work_count"] = count
            selected.append(source)

    if config.target_journal and not selected:
        tqdm.write(f"warning: target journal {config.target_journal!r} did not match any sampled sources")
    return selected


def fetch_works(config: Config, client: OpenAlexClient, sources: list[dict[str, Any]]) -> list[dict[str, Any]]:
    cached = raw_path(config, "works")
    if cached.exists() and not config.refresh:
        return load_jsonl(cached)

    works: list[dict[str, Any]] = []
    seen_ids: set[str] = set()
    sources_by_publisher: dict[str, list[dict[str, Any]]] = {}
    for source in sources:
        publisher_id = source.get("_publisher_id") or "unknown"
        sources_by_publisher.setdefault(publisher_id, []).append(source)

    for publisher_id, publisher_sources in tqdm(
        sources_by_publisher.items(), desc="works", unit="publisher"
    ):
        fetched_for_publisher = 0
        per_source_limit = max(
            1, (config.max_works_per_publisher + len(publisher_sources) - 1) // len(publisher_sources)
        )
        for source in publisher_sources:
            if fetched_for_publisher >= config.max_works_per_publisher:
                break
            source_id = openalex_id(source.get("id"))
            if not source_id:
                continue
            fetch_limit = min(per_source_limit, config.max_works_per_publisher - fetched_for_publisher)
            work_filter = ",".join(
                [
                    f"from_publication_date:{config.start_date}",
                    f"to_publication_date:{config.end_date}",
                    "type:article|review",
                    f"primary_location.source.id:{source_id}",
                    f"title_and_abstract.search:{config.domain_query}",
                ]
            )
            params = {
                "filter": work_filter,
                "sort": "cited_by_count:desc",
            }
            try:
                source_works = client.list_cursor(
                    "works",
                    params,
                    limit=fetch_limit,
                    desc=f"works {source.get('display_name', source_id)[:24]}",
                )
            except OpenAlexError as error:
                tqdm.write(f"warning: works lookup failed for {source.get('display_name')}: {error}")
                continue
            for work in source_works:
                work_id = work.get("id")
                if work_id and work_id not in seen_ids:
                    work["_selected_source_id"] = source.get("id")
                    work["_selected_source_name"] = source.get("display_name")
                    work["_selected_publisher_id"] = publisher_id
                    work["_selected_publisher_name"] = source.get("_publisher_name")
                    seen_ids.add(work_id)
                    works.append(work)
                    fetched_for_publisher += 1

    write_jsonl(cached, works)
    return works


def abstract_text(index: dict[str, list[int]] | None) -> str | None:
    if not index:
        return None
    positions: dict[int, str] = {}
    for word, word_positions in index.items():
        for position in word_positions:
            positions[position] = word
    return " ".join(positions[position] for position in sorted(positions))


def source_from_work(work: dict[str, Any]) -> dict[str, Any]:
    primary_location = work.get("primary_location") or {}
    return primary_location.get("source") or {}


def normalize_publishers(records: list[dict[str, Any]]) -> pd.DataFrame:
    columns = [
        "publisher_id",
        "publisher_openalex_id",
        "display_name",
        "query_name",
        "country_codes",
        "works_count",
        "cited_by_count",
        "homepage_url",
    ]
    rows = []
    for item in records:
        rows.append(
            {
                "publisher_id": item.get("id"),
                "publisher_openalex_id": openalex_id(item.get("id")),
                "display_name": item.get("display_name"),
                "query_name": item.get("_query_name"),
                "country_codes": "|".join(item.get("country_codes") or []),
                "works_count": item.get("works_count"),
                "cited_by_count": item.get("cited_by_count"),
                "homepage_url": item.get("homepage_url"),
            }
        )
    return pd.DataFrame(rows, columns=columns)


def normalize_sources(records: list[dict[str, Any]]) -> pd.DataFrame:
    columns = [
        "source_id",
        "source_openalex_id",
        "display_name",
        "issn_l",
        "issn",
        "type",
        "publisher_id",
        "publisher_name",
        "works_count",
        "cited_by_count",
        "is_oa",
        "is_in_doaj",
        "h_index",
        "i10_index",
        "domain_match_method",
        "domain_work_count",
    ]
    rows = []
    for item in records:
        summary_stats = item.get("summary_stats") or {}
        rows.append(
            {
                "source_id": item.get("id"),
                "source_openalex_id": openalex_id(item.get("id")),
                "display_name": item.get("display_name"),
                "issn_l": item.get("issn_l"),
                "issn": "|".join(item.get("issn") or []),
                "type": item.get("type"),
                "publisher_id": item.get("_publisher_id") or item.get("host_organization"),
                "publisher_name": item.get("_publisher_name") or item.get("host_organization_name"),
                "works_count": item.get("works_count"),
                "cited_by_count": item.get("cited_by_count"),
                "is_oa": item.get("is_oa"),
                "is_in_doaj": item.get("is_in_doaj"),
                "h_index": summary_stats.get("h_index"),
                "i10_index": summary_stats.get("i10_index"),
                "domain_match_method": item.get("_domain_match_method"),
                "domain_work_count": item.get("_domain_work_count"),
            }
        )
    return pd.DataFrame(rows, columns=columns)


def normalize_works(records: list[dict[str, Any]]) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    work_columns = [
        "work_id",
        "work_openalex_id",
        "doi",
        "title",
        "publication_date",
        "publication_year",
        "type",
        "cited_by_count",
        "is_retracted",
        "is_oa",
        "oa_status",
        "oa_url",
        "any_repository_has_fulltext",
        "primary_source_id",
        "primary_source_name",
        "primary_source_issn_l",
        "primary_source_issn",
        "primary_source_publisher",
        "selected_source_id",
        "selected_source_name",
        "selected_publisher_id",
        "selected_publisher_name",
        "abstract",
    ]
    authorship_columns = [
        "work_id",
        "author_id",
        "author_name",
        "author_position",
        "is_corresponding",
        "raw_affiliation_string",
    ]
    institution_columns = [
        "work_id",
        "author_id",
        "institution_id",
        "institution_name",
        "country_code",
        "ror",
        "type",
    ]
    topic_columns = [
        "work_id",
        "topic_id",
        "topic_name",
        "subfield",
        "field",
        "domain",
        "score",
    ]
    funder_columns = [
        "work_id",
        "funder_id",
        "funder_name",
        "award_id",
    ]
    work_rows: list[dict[str, Any]] = []
    authorship_rows: list[dict[str, Any]] = []
    institution_rows: list[dict[str, Any]] = []
    topic_rows: list[dict[str, Any]] = []
    funder_rows: list[dict[str, Any]] = []

    for work in records:
        work_id = work.get("id")
        source = source_from_work(work)
        open_access = work.get("open_access") or {}
        work_rows.append(
            {
                "work_id": work_id,
                "work_openalex_id": openalex_id(work_id),
                "doi": work.get("doi"),
                "title": work.get("title") or work.get("display_name"),
                "publication_date": work.get("publication_date"),
                "publication_year": work.get("publication_year"),
                "type": work.get("type"),
                "cited_by_count": work.get("cited_by_count"),
                "is_retracted": work.get("is_retracted"),
                "is_oa": open_access.get("is_oa"),
                "oa_status": open_access.get("oa_status"),
                "oa_url": open_access.get("oa_url"),
                "any_repository_has_fulltext": open_access.get("any_repository_has_fulltext"),
                "primary_source_id": source.get("id"),
                "primary_source_name": source.get("display_name"),
                "primary_source_issn_l": source.get("issn_l"),
                "primary_source_issn": "|".join(source.get("issn") or []),
                "primary_source_publisher": source.get("host_organization_name"),
                "selected_source_id": work.get("_selected_source_id"),
                "selected_source_name": work.get("_selected_source_name"),
                "selected_publisher_id": work.get("_selected_publisher_id"),
                "selected_publisher_name": work.get("_selected_publisher_name"),
                "abstract": abstract_text(work.get("abstract_inverted_index")),
            }
        )

        for authorship in work.get("authorships") or []:
            author = authorship.get("author") or {}
            author_id = author.get("id")
            authorship_rows.append(
                {
                    "work_id": work_id,
                    "author_id": author_id,
                    "author_name": author.get("display_name"),
                    "author_position": authorship.get("author_position"),
                    "is_corresponding": authorship.get("is_corresponding"),
                    "raw_affiliation_string": "; ".join(authorship.get("raw_affiliation_strings") or []),
                }
            )
            for institution in authorship.get("institutions") or []:
                institution_rows.append(
                    {
                        "work_id": work_id,
                        "author_id": author_id,
                        "institution_id": institution.get("id"),
                        "institution_name": institution.get("display_name"),
                        "country_code": institution.get("country_code"),
                        "ror": institution.get("ror"),
                        "type": institution.get("type"),
                    }
                )

        for topic in work.get("topics") or []:
            topic_rows.append(
                {
                    "work_id": work_id,
                    "topic_id": topic.get("id"),
                    "topic_name": topic.get("display_name"),
                    "subfield": ((topic.get("subfield") or {}).get("display_name")),
                    "field": ((topic.get("field") or {}).get("display_name")),
                    "domain": ((topic.get("domain") or {}).get("display_name")),
                    "score": topic.get("score"),
                }
            )

        for grant in work.get("grants") or []:
            funder_rows.append(
                {
                    "work_id": work_id,
                    "funder_id": grant.get("funder"),
                    "funder_name": grant.get("funder_display_name"),
                    "award_id": grant.get("award_id"),
                }
            )

    return (
        pd.DataFrame(work_rows, columns=work_columns),
        pd.DataFrame(authorship_rows, columns=authorship_columns),
        pd.DataFrame(institution_rows, columns=institution_columns),
        pd.DataFrame(topic_rows, columns=topic_columns),
        pd.DataFrame(funder_rows, columns=funder_columns),
    )


def write_parquet(path: Path, frame: pd.DataFrame) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = path.with_suffix(path.suffix + ".tmp")
    frame.to_parquet(tmp_path, index=False)
    tmp_path.replace(path)


def save_normalized(config: Config, publishers: list[dict[str, Any]], sources: list[dict[str, Any]], works: list[dict[str, Any]]) -> None:
    publisher_frame = normalize_publishers(publishers)
    source_frame = normalize_sources(sources)
    work_frame, authorship_frame, institution_frame, topic_frame, funder_frame = normalize_works(works)
    frames = {
        "publishers": publisher_frame,
        "sources": source_frame,
        "works": work_frame,
        "authorships": authorship_frame,
        "institutions": institution_frame,
        "work_topics": topic_frame,
        "work_funders": funder_frame,
    }
    for name, frame in tqdm(frames.items(), desc="parquet", unit="table"):
        write_parquet(parquet_path(config, name), frame)


def create_duckdb(config: Config) -> None:
    db_path = config.out_dir / "openalex_mvp.duckdb"
    db_path.parent.mkdir(parents=True, exist_ok=True)
    connection = duckdb.connect(str(db_path))
    try:
        for name in PARQUET_NAMES:
            path = parquet_path(config, name)
            connection.execute(
                f"CREATE OR REPLACE TABLE {name} AS SELECT * FROM read_parquet(?)",
                [str(path)],
            )
    finally:
        connection.close()


def summarize(config: Config, publishers: list[dict[str, Any]], sources: list[dict[str, Any]], works: list[dict[str, Any]]) -> dict[str, Any]:
    db_path = config.out_dir / "openalex_mvp.duckdb"
    summary: dict[str, Any] = {
        "publishers": len(publishers),
        "sources": len(sources),
        "works": len(works),
        "raw_dir": str(config.out_dir / "raw"),
        "parquet_dir": str(config.out_dir / "parquet"),
        "duckdb": str(db_path),
    }
    if not works:
        return summary
    connection = duckdb.connect(str(db_path), read_only=True)
    try:
        row = connection.execute(
            """
            SELECT
              COUNT(DISTINCT primary_source_id) AS journals,
              SUM(CASE WHEN is_oa THEN 1 ELSE 0 END) AS open_access_works,
              SUM(CASE WHEN is_retracted THEN 1 ELSE 0 END) AS retracted_works,
              SUM(CASE WHEN abstract IS NOT NULL THEN 1 ELSE 0 END) AS works_with_abstracts,
              COALESCE(SUM(cited_by_count), 0) AS total_citations
            FROM works
            """
        ).fetchone()
        summary.update(
            {
                "journals_with_works": row[0],
                "open_access_works": row[1],
                "retracted_works": row[2],
                "works_with_abstracts": row[3],
                "total_citations": row[4],
            }
        )
    finally:
        connection.close()
    return summary


def run(config: Config) -> dict[str, Any]:
    (config.out_dir / "raw").mkdir(parents=True, exist_ok=True)
    (config.out_dir / "parquet").mkdir(parents=True, exist_ok=True)
    client = OpenAlexClient(config.email)

    publishers = fetch_publishers(config, client)
    sources = fetch_candidate_sources(config, client, publishers)
    works = fetch_works(config, client, sources)
    save_normalized(config, publishers, sources, works)
    create_duckdb(config)
    return summarize(config, publishers, sources, works)


def print_summary(summary: dict[str, Any], output_format: str) -> None:
    if output_format == "json":
        print(json.dumps(summary, indent=2, sort_keys=True))
        return
    print("\nOpenAlex download summary")
    for key, value in summary.items():
        print(f"- {key}: {value}")


def main(argv: list[str] | None = None) -> int:
    try:
        config = parse_args(argv)
        summary = run(config)
        print_summary(summary, config.format)
        return 0
    except KeyboardInterrupt:
        print("Interrupted; completed raw/parquet files remain cached for the next run.", file=sys.stderr)
        return 130
    except OpenAlexError as error:
        print(f"error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
