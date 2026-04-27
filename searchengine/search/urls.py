from django.urls import path

from .views import search_documents

urlpatterns = [
    path("", search_documents, name="search-documents"),
]
