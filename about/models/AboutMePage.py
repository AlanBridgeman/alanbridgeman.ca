from django.db import models

from wagtail import blocks
from wagtail.admin.panels import FieldPanel
from wagtail.contrib.table_block.blocks import TableBlock
from wagtail.fields import StreamField
from wagtail.images.blocks import ImageChooserBlock
from wagtail.models import Page

class AboutMePage(Page):
    body = StreamField([
        ('heading', blocks.CharBlock(form_classname="title")),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
        ('table', TableBlock()),
    ], use_json_field=True, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('body')
    ]

    def get_context(self, request):
        context = super().get_context(request)
        context['children'] = self.get_children().live().first()
        return context

    parent_page_types = ['home.HomePage']