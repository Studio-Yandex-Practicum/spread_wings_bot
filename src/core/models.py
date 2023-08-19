from django.db import models
from transliterate import translit

from core.utils import to_snake_case


class BaseModel(models.Model):
    """Base model."""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:  # noqa
        abstract = True


class Region(BaseModel):
    """Region model."""

    region_name = models.CharField(max_length=200, unique=True)
    region_key = models.CharField(max_length=200, unique=True)

    def save(
        self,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None,
    ):
        """Save method."""
        self.region_key = to_snake_case(
            translit(self.region_name, reversed=True)
        )
        return super(Region, self).save(
            force_insert, force_update, using, update_fields
        )

    def __str__(self):
        return self.region_name

    class Meta:  # noqa
        verbose_name = "Регион"
        verbose_name_plural = "Регионы"
        ordering = ("region_name",)
