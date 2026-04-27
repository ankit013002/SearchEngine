from django.db import models


class Document(models.Model):
    title = models.CharField(max_length=255)
    url = models.URLField(unique=True)
    content = models.TextField()
    last_indexed_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-last_indexed_at", "id"]
        indexes = [
            models.Index(fields=["title"]),
            models.Index(fields=["last_indexed_at"]),
        ]

    def __str__(self) -> str:
        return self.title
