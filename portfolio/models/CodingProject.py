from django.db import models

from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel

from wagtail.admin.panels import FieldPanel
from wagtail.models import Orderable

from .CodingPortfolioPage import CodingPortfolioPage

class CodingProject(ClusterableModel, Orderable):
    page = ParentalKey(CodingPortfolioPage, on_delete=models.DO_NOTHING, related_name='projects')
    repository_link = models.URLField(blank=True, null=True)

    panels = [
        FieldPanel('repository_link', heading="Repository")
    ]

    class Meta:
        verbose_name = "Coding Project"
        verbose_name_plural = "Coding Projects"