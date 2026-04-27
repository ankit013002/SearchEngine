from django.http import JsonResponse
from django.views.decorators.http import require_GET

from .models import Document

DEFAULT_LIMIT = 10
MAX_LIMIT = 50


def _parse_limit(raw_limit: str | None) -> int:
    if raw_limit in (None, ""):
        return DEFAULT_LIMIT

    parsed_limit = int(raw_limit)
    if parsed_limit < 1:
        raise ValueError("limit must be >= 1")

    return min(parsed_limit, MAX_LIMIT)


@require_GET
def search_documents(request):
    query = (request.GET.get("q") or "").strip()

    if not query:
        return JsonResponse(
            {"query": query, "count": 0, "results": [], "limit": DEFAULT_LIMIT}
        )

    try:
        limit = _parse_limit(request.GET.get("limit"))
    except ValueError:
        return JsonResponse(
            {"error": "Invalid 'limit' parameter. Use a positive integer."}, status=400
        )

    docs = Document.objects.filter(title__icontains=query) | Document.objects.filter(
        content__icontains=query
    )

    results = []
    lowered_query = query.lower()
    for document in docs.distinct()[:200]:
        title_hits = document.title.lower().count(lowered_query)
        content_hits = document.content.lower().count(lowered_query)
        score = (title_hits * 3) + content_hits
        if score > 0:
            snippet = document.content[:180]
            results.append(
                {
                    "title": document.title,
                    "url": document.url,
                    "score": score,
                    "snippet": snippet,
                }
            )

    sorted_results = sorted(
        results,
        key=lambda item: (-item["score"], item["title"].lower(), item["url"]),
    )[:limit]

    return JsonResponse(
        {
            "query": query,
            "limit": limit,
            "count": len(sorted_results),
            "results": sorted_results,
        }
    )
