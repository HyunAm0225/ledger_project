from django.db import models


class BaseModel(models.Model):
    id = models.BigAutoField(
        db_index=True,
        unique=True,
        primary_key=True,
        auto_created=True,
        verbose_name="ID",
    )
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("pk",)
        abstract = True

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
