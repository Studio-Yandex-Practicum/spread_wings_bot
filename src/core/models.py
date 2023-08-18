from django.db import models


class BaseModel(models.Model):
    """Base model."""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Region(BaseModel):
    """Region model."""

    region_name = models.CharField(max_length=200, unique=True)
    region_key = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.region_name

    class Meta:
        verbose_name = "Регион"
        verbose_name_plural = "Регионы"
        ordering = ("region_name",)
