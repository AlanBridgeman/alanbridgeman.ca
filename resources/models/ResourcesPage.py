from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, path
from wagtail.contrib.table_block.blocks import TableBlock
from wagtail import blocks
from wagtail.fields import StreamField
from wagtail.images.blocks import ImageChooserBlock
from wagtail.models import Page

from .Podcast import Podcast

class ResourcesPage(RoutablePageMixin, Page):
    body = StreamField([
        ('heading', blocks.CharBlock(form_classname="title")),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
        ('table', TableBlock()),
        ('podcast', Podcast())
    ], use_json_field=True, blank=True)
    
    content_panels = Page.content_panels + [
        FieldPanel('body')
    ]

    parent_page_types = ['home.HomePage']

    @path('') # This is the default path
    def default(self, request):
        return self.serve(request)
