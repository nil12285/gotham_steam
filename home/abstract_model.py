from django.db import models
from django.utils.text import slugify

class AbstractBaseFilterModel(models.Model):
    """
    Base model for all dynamic filter choices like ProgramType, Location, etc.
    """
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True, max_length=255, editable=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True
        ordering = ['name']

