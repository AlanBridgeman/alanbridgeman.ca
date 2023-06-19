from django.db import models

from wagtail import blocks
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, path
from wagtail.contrib.table_block.blocks import TableBlock
from wagtail.fields import StreamField
from wagtail.images.blocks import ImageChooserBlock
from wagtail.models import Page

class ProfessionalExperiencePage(RoutablePageMixin, Page):
    body = StreamField([
        ('heading', blocks.CharBlock(form_classname="title")),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
        ('table', TableBlock()),
    ], use_json_field=True, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('body'),
        InlinePanel('experiences', label="Experience")
    ]

    parent_page_types = ['about.AboutMePage']
    subpage_types = []

    @path('') # This is the default path
    def index(self, request):
        return self.render(request)