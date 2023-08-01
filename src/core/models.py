from django.db import models


class BaseModel(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Region(BaseModel):

    region_name = models.CharField(max_length=200, unique=True)
    region_key = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.region_name