from django.db import models

from wagtail import blocks
from wagtail.admin.panels import FieldPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, path
from wagtail.fields import StreamField
from wagtail.images.blocks import ImageChooserBlock
from wagtail.models import Page

from .Newsletter import Newsletter

class NewsletterPage(RoutablePageMixin, Page):
    body = StreamField([
        ('heading', blocks.CharBlock(classname="full title")),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock())
    ], use_json_field=True, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('body'),
    ]

    parent_page_types = ['home.HomePage']

    @path('')  # This is the default path
    def get_index(self, request):
        context = self.get_context(request)

        context['issues'] = Newsletter.objects.live().order_by('-date')

        return self.render(request, context_overrides=context)
    
    @path('issue/<date>/')
    def get_issue(self, request, date):
        """Get the newsletter issue for the given date.

        Args:
            request (object): The request object.
            date (date): The date of the newsletter issue to get.

        Returns:
            string: The newsletter issue for the given date as an HTML page.
        """
        context = self.get_context(request)

        # Override the page object with the newsletter issue for the given date
        context['page'] = Newsletter.objects.live().filter(date=date).first()

        return self.render(request, template='newsletter/issue.html', context_overrides=context)
