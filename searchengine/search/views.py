from django.http import JsonResponse
from django.views.decorators.http import require_GET

from .models import Document


@require_GET
def search_documents(request):
    query = (request.GET.get("q") or "").strip()

    if not query:
        return JsonResponse({"query": query, "count": 0, "results": []})

    limit = min(int(request.GET.get("limit", "10")), 50)

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

    sorted_results = sorted(results, key=lambda item: item["score"], reverse=True)[:limit]
    return JsonResponse(
        {
            "query": query,
            "count": len(sorted_results),
            "results": sorted_results,
        }
    )
