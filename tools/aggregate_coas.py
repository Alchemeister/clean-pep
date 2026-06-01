#!/usr/bin/env python3
"""Discover public COA/test-report candidate URLs without creating COA claims.

The output is a candidate queue. A candidate becomes a COA record only after a
human or parser verifies product, vendor, batch, test date, and panel fields.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from typing import Iterable
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen


KEYWORDS = (
    "coa",
    "coas",
    "certificate",
    "analysis",
    "test",
    "testing",
    "lab",
    "janoshik",
    "pdf",
    "purity",
    "solvent",
    "residual",
    "tfa",
    "endotoxin",
    "heavy-metal",
    "heavy metal",
    "sterility",
)


class LinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[tuple[str, str]] = []
        self._href: str | None = None
        self._text: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() != "a":
            return
        href = dict(attrs).get("href")
        if href:
            self._href = href
            self._text = []

    def handle_data(self, data: str) -> None:
        if self._href:
            self._text.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "a" and self._href:
            self.links.append((self._href, " ".join(self._text).strip()))
            self._href = None
            self._text = []


@dataclass(frozen=True)
class Source:
    vendor: str
    url: str
    type: str
    product: str | None = None


def load_sources(path: Path) -> list[Source]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    return [Source(**item) for item in raw["sources"]]


def fetch(url: str, timeout: int) -> str:
    request = Request(
        url,
        headers={
            "User-Agent": "CleanPep COA discovery bot (+manual verification required)",
            "Accept": "text/html,application/xhtml+xml,application/pdf;q=0.8,*/*;q=0.5",
        },
    )
    with urlopen(request, timeout=timeout) as response:
        content_type = response.headers.get("content-type", "")
        body = response.read(2_000_000)
    if "pdf" in content_type.lower() or url.lower().endswith(".pdf"):
        return ""
    return body.decode("utf-8", errors="replace")


def score_candidate(href: str, text: str) -> int:
    haystack = f"{href} {text}".lower()
    return sum(1 for keyword in KEYWORDS if keyword in haystack)


def discover(source: Source, timeout: int) -> list[dict[str, object]]:
    html = fetch(source.url, timeout)
    parser = LinkParser()
    parser.feed(html)
    seen: set[str] = set()
    candidates = []
    for href, text in parser.links:
        absolute = urljoin(source.url, href)
        parsed = urlparse(absolute)
        if parsed.scheme not in {"http", "https"}:
            continue
        score = score_candidate(absolute, text)
        if score == 0:
            continue
        key = re.sub(r"#.*$", "", absolute)
        if key in seen:
            continue
        seen.add(key)
        candidates.append(
            {
                "vendor": source.vendor,
                "product_hint": source.product,
                "source_url": source.url,
                "candidate_url": absolute,
                "anchor_text": text,
                "score": score,
                "status": "candidate-unverified",
            }
        )
    return sorted(candidates, key=lambda item: (-int(item["score"]), str(item["candidate_url"])))


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main(argv: Iterable[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sources", default="data/coa_sources.json")
    parser.add_argument("--out", default="data/coa_candidates.json")
    parser.add_argument("--timeout", type=int, default=15)
    args = parser.parse_args(list(argv))

    sources = load_sources(Path(args.sources))
    all_candidates: list[dict[str, object]] = []
    errors: list[dict[str, str]] = []
    for source in sources:
        try:
            all_candidates.extend(discover(source, args.timeout))
        except Exception as exc:  # noqa: BLE001 - keep batch discovery moving.
            errors.append({"vendor": source.vendor, "url": source.url, "error": str(exc)})

    payload = {
        "schema_version": 1,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "record_type": "candidate_queue_not_verified_coas",
        "candidates": all_candidates,
        "errors": errors,
    }
    write_json(Path(args.out), payload)
    print(f"wrote {len(all_candidates)} candidates and {len(errors)} errors to {args.out}")
    return 1 if errors and not all_candidates else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
