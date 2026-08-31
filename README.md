# JS Endpoint Extractor

A lightweight static JavaScript analyzer designed to reduce noise from bundled/minified JS.

## Extracts

- Absolute HTTP/HTTPS URLs
- WebSocket URLs
- Relative paths / endpoint-like paths
- GraphQL references
- Hostnames
- Query parameter names

## Cleaner output

The extractor avoids treating normal JavaScript property access such as:

```text
.getClient
.pathname
.token
```

as parameters. Query parameters are extracted only from actual query-string patterns.

## Usage

```bash
python jsextract.py -f app.js
python jsextract.py -u https://example.com/app.js
python jsextract.py -f app.js -o endpoints.txt
```

Only analyze JavaScript you own or are authorized to test.
