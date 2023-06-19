from django.db import models

from wagtail import blocks
from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField
from wagtail.images.blocks import ImageChooserBlock
from wagtail.models import Page

class Newsletter(Page):
    date = models.DateField()
    body = StreamField([
        ('heading', blocks.CharBlock(classname="full title")),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock())
    ], use_json_field=True, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('date'),
        FieldPanel('body'),
    ]

    parent_page_types = ['newsletter.NewsletterPage']

    template = 'newsletter/issue.html'