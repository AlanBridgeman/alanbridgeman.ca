from django.db import models

from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel

from wagtail.admin.panels import FieldPanel
from wagtail.contrib.table_block.blocks import TableBlock
from wagtail import blocks
from wagtail.fields import StreamField
from wagtail.images.blocks import ImageChooserBlock
from wagtail.models import Orderable

from .CreativePortfolioPage import CreativePortfolioPage

class PhotoArt(ClusterableModel, Orderable):
    page = ParentalKey(CreativePortfolioPage, on_delete=models.DO_NOTHING, related_name='photo_art')
    title = models.CharField(max_length=255, blank=True, null=True)
    description = StreamField([
        ('heading', blocks.CharBlock(form_classname="title")),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
        ('table', TableBlock()),
    ], use_json_field=True, blank=True)
    image = models.ForeignKey('wagtailimages.Image', on_delete=models.CASCADE, related_name='+', blank=False)

    panels = [
        FieldPanel('title'),
        FieldPanel('description'),
        FieldPanel('image')
    ]

    class Meta:
        verbose_name = "Photo Art"
        verbose_name_plural = "Photo Art"