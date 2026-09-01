
"""JS Endpoint Extractor - cleaner static extraction for bundled JavaScript."""

import argparse
import re
import sys
from pathlib import Path
import urllib.request
from urllib.parse import urlparse


URL_RE = re.compile(r"""["']((?:https?|wss?)://[^"'<>\\\s]+)["']""", re.I)
PATH_RE = re.compile(
    r"""["']((?:/(?!/)|\./|\.\./)[A-Za-z0-9_./:@?&=%+\-~]+)["']"""
)
DOMAIN_RE = re.compile(
    r"""(?<![@\w.-])((?:[a-z0-9-]+\.)+
    (?:com|net|org|io|dev|app|co|in|ai|me|tech|xyz|cloud))(?![\w.-])""",
    re.I | re.X,
)
GRAPHQL_RE = re.compile(r"""["']([^"'\\\s]*graphql[^"'\\\s]*)["']""", re.I)

QUERY_PARAM_RE = re.compile(r"""[?&]([A-Za-z][A-Za-z0-9_.-]{1,40})(?:=|&|$)""")

EXTENSION_RE = re.compile(
    r"""\.(?:js|json|xml|txt|csv|yaml|yml|map|graphql)(?:[?#]|$)""", re.I
)

def clean(value):
    return value.rstrip(".,;)]}")

def extract(text):
    out = {k: set() for k in (
        "urls", "paths", "domains", "websockets", "graphql", "parameters"
    )}

    for value in URL_RE.findall(text):
        value = clean(value)
        out["urls"].add(value)
        if value.lower().startswith(("ws://", "wss://")):
            out["websockets"].add(value)
        try:
            parsed = urlparse(value)
            if parsed.hostname:
                out["domains"].add(parsed.hostname.lower())
            for match in QUERY_PARAM_RE.finditer(parsed.query):
                out["parameters"].add(match.group(1))
        except ValueError:
            pass

    for value in PATH_RE.findall(text):
        value = clean(value)
     
        if len(value) < 2:
            continue
        if value.startswith(("/static/", "/assets/")) and not EXTENSION_RE.search(value):
            continue
        out["paths"].add(value)
        for match in QUERY_PARAM_RE.finditer(value):
            out["parameters"].add(match.group(1))

    for value in DOMAIN_RE.findall(text):
        out["domains"].add(value.lower())

    for value in GRAPHQL_RE.findall(text):
        value = clean(value)
        if value.startswith(("/", "http://", "https://")) or "graphql" in value.lower():
            out["graphql"].add(value)

    return {k: sorted(v) for k, v in out.items()}

def print_results(results):
    sections = [
        ("urls", "URLs"),
        ("websockets", "WebSocket URLs"),
        ("paths", "Paths / Endpoints"),
        ("graphql", "GraphQL References"),
        ("domains", "Domains"),
        ("parameters", "Query Parameters"),
    ]
    total = sum(len(v) for v in results.values())
    print(f"\n[+] Found {total} references")
    for key, title in sections:
        if results[key]:
            print(f"\n[{title}]")
            for item in results[key]:
                print(f"  {item}")

def main():
    parser = argparse.ArgumentParser(
        description="Extract useful references from JavaScript."
    )
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("-f", "--file", help="Local JavaScript file")
    source.add_argument("-u", "--url", help="JavaScript URL (authorized targets only)")
    parser.add_argument("-o", "--output", help="Save extracted references")
    args = parser.parse_args()

    try:
        if args.file:
            text = Path(args.file).read_text(encoding="utf-8", errors="ignore")
        else:
            req = urllib.request.Request(
                args.url,
                headers={"User-Agent": "JS-Endpoint-Extractor/1.1"},
            )
            with urllib.request.urlopen(req, timeout=15) as response:
                text = response.read().decode("utf-8", errors="ignore")
    except Exception as exc:
        print(f"[-] Error: {exc}", file=sys.stderr)
        return 1

    results = extract(text)
    print_results(results)

    if args.output:
        lines = []
        for key in ("urls", "websockets", "paths", "graphql", "domains", "parameters"):
            lines.extend(results[key])
        Path(args.output).write_text(
            "\n".join(dict.fromkeys(lines)) + ("\n" if lines else ""),
            encoding="utf-8",
        )
        print(f"\n[+] Saved results to {args.output}")

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
