from django.db import models

from wagtail.admin.panels import FieldPanel
from wagtail.models import Page
from wagtail.fields import RichTextField

class HomePage(Page):
    welcome_message = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('welcome_message', classname="full"),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        context['children'] = self.get_children().live()
        return context