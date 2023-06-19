from wagtail.admin.panels import InlinePanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, path
from wagtail.models import Page

class CodingPortfolioPage(RoutablePageMixin, Page):
    content_panels = Page.content_panels + [
        InlinePanel('projects', label="Projects")
    ]

    parent_page_types = ['portfolio.PortfolioPage']

    @path('') # This is the default path
    def default(self, request):
        return self.serve(request)