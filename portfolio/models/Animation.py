from django.db import models

from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail import blocks
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.contrib.table_block.blocks import TableBlock
from wagtail.fields import StreamField
from wagtail.images.blocks import ImageChooserBlock
from wagtail.models import Orderable

from wagtailvideos.edit_handlers import VideoChooserPanel

from .CreativePortfolioPage import CreativePortfolioPage

class Animation(ClusterableModel, Orderable):
    page = ParentalKey(CreativePortfolioPage, on_delete=models.DO_NOTHING, related_name='animations')
    title = models.CharField(max_length=255, blank=True, null=True)
    demo = models.ForeignKey('wagtailvideos.Video', on_delete=models.SET_NULL, related_name='animation_demo', blank=True, null=True)
    description = StreamField([
        ('heading', blocks.CharBlock(form_classname="title")),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
        ('table', TableBlock()),
    ], use_json_field=True, blank=True)

    panels = [
        FieldPanel('title'),
        InlinePanel('raw_files', label="Raw Files"),
        VideoChooserPanel('demo'),
        FieldPanel('description')
    ]

    class Meta:
        verbose_name = "Animation"
        verbose_name_plural = "Animations"

class RawFiles(Orderable):
    animation = ParentalKey(Animation, on_delete=models.CASCADE, related_name='raw_files')
    raw_file = models.ForeignKey('wagtaildocs.Document', on_delete=models.CASCADE, related_name='+')

    panels = [
        FieldPanel('raw_file'),
    ]

    class Meta:
        verbose_name = "Raw File"
        verbose_name_plural = "Raw Files"