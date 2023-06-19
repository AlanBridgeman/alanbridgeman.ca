from django.db import models

from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel

from wagtail import blocks
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.contrib.table_block.blocks import TableBlock
from wagtail.models import Orderable
from wagtail.fields import StreamField
from wagtail.images.blocks import ImageChooserBlock


from .VolunteerExperiencePage import VolunteerExperiencePage

class VolunteerExperience(Orderable, ClusterableModel):
    page = ParentalKey(VolunteerExperiencePage, on_delete=models.DO_NOTHING, related_name='experiences')
    position = models.CharField(max_length=250, blank=False)
    organization = models.CharField(max_length=250, blank=False)
    org_logo = models.ForeignKey('wagtailimages.Image', on_delete=models.SET_NULL, related_name='volunteer_org_logo', null=True)
    start_date = models.DateField(blank=False)
    end_date = models.DateField(blank=True, null=True)
    description = StreamField([
        ('heading', blocks.CharBlock(form_classname="title")),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
        ('table', TableBlock()),
    ], use_json_field=True, blank=True)

    panels = [
        FieldPanel('position'),
        MultiFieldPanel([
            FieldPanel('organization'),
            FieldPanel('org_logo'),
        ], heading="Organization"),
        MultiFieldPanel([
            FieldPanel('start_date'),
            FieldPanel('end_date'),
        ], heading="Dates"),
        FieldPanel('description'),
    ]

    class Meta:
        verbose_name = "Experience"
        verbose_name_plural = "Experiences"
