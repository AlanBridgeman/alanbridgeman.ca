from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, path
from wagtail.contrib.table_block.blocks import TableBlock
from wagtail.core import blocks
from wagtail.fields import StreamField
from wagtail.images.blocks import ImageChooserBlock
from wagtail.models import Page

class CreativePortfolioPage(RoutablePageMixin, Page):
    body = StreamField([
        ('heading', blocks.CharBlock(form_classname="title")),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
        ('table', TableBlock()),
    ], use_json_field=True, blank=True)
    
    content_panels = Page.content_panels + [
        FieldPanel('body'),
        InlinePanel('animations', label="Animations"),
        InlinePanel('photo_art', label="Photo Art")
    ]

    parent_page_types = ['portfolio.PortfolioPage']

    @path('') # This is the default path
    def default(self, request):
        return self.serve(request)