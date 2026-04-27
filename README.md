# SearchEngine

A lightweight Django-based search API project with crawler/indexer/search apps.

## Quick start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python searchengine/manage.py migrate
python searchengine/manage.py runserver
```

## Search endpoint

`GET /search/?q=<query>&limit=<n>`

Example:

```bash
curl "http://127.0.0.1:8000/search/?q=search&limit=5"
```

Response includes ranked results with title, url, snippet, and score.
