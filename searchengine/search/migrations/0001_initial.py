from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Document",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=255)),
                ("url", models.URLField(unique=True)),
                ("content", models.TextField()),
                ("last_indexed_at", models.DateTimeField(auto_now=True)),
            ],
            options={"ordering": ["-last_indexed_at", "id"]},
        ),
        migrations.AddIndex(
            model_name="document",
            index=models.Index(fields=["title"], name="search_docum_title_7738d5_idx"),
        ),
        migrations.AddIndex(
            model_name="document",
            index=models.Index(fields=["last_indexed_at"], name="search_docum_last_in_418d85_idx"),
        ),
    ]
