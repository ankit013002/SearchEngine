from django.test import TestCase
from django.urls import reverse

from .models import Document


class SearchDocumentsTests(TestCase):
    def setUp(self):
        Document.objects.create(
            title="Python search guide",
            url="https://example.com/python-search",
            content="A practical guide to building a search engine with Python.",
        )
        Document.objects.create(
            title="Ranking content",
            url="https://example.com/ranking",
            content="Ranking in a search engine depends on relevance and search intent.",
        )

    def test_empty_query_returns_no_results(self):
        response = self.client.get(reverse("search-documents"))

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["count"], 0)
        self.assertEqual(payload["limit"], 10)

    def test_query_returns_ranked_results(self):
        response = self.client.get(reverse("search-documents"), {"q": "search"})

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["query"], "search")
        self.assertEqual(payload["count"], 2)
        self.assertEqual(payload["results"][0]["title"], "Python search guide")

    def test_limit_caps_result_count(self):
        response = self.client.get(reverse("search-documents"), {"q": "search", "limit": 1})

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["count"], 1)
        self.assertEqual(payload["limit"], 1)

    def test_non_numeric_limit_returns_bad_request(self):
        response = self.client.get(reverse("search-documents"), {"q": "search", "limit": "abc"})

        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid 'limit'", response.json()["error"])

    def test_negative_limit_returns_bad_request(self):
        response = self.client.get(reverse("search-documents"), {"q": "search", "limit": -5})

        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid 'limit'", response.json()["error"])

    def test_limit_over_maximum_is_clamped(self):
        response = self.client.get(reverse("search-documents"), {"q": "search", "limit": 999})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["limit"], 50)
