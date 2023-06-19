from datetime import date

from django.db import models
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from modelcluster.fields import ParentalKey

from wagtail import blocks
from wagtail.admin.panels import FieldPanel, FieldRowPanel, InlinePanel, MultiFieldPanel
from wagtail.admin.mail import send_mail
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.fields import StreamField, RichTextField
from wagtail.images.blocks import ImageChooserBlock

from mailchimp_marketing import Client
from mailchimp_marketing.api_client import ApiClientError

class FormField(AbstractFormField):
    page = ParentalKey('newsletter.SubscribePage', on_delete=models.CASCADE, related_name='form_fields')


class SubscribePage(AbstractEmailForm):
    body = StreamField([
        ('heading', blocks.CharBlock(classname="full title")),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock())
    ], use_json_field=True, blank=True)
    thank_you_text = RichTextField(blank=True)
    auto_register_to_mailchimp = models.BooleanField(default=True)

    content_panels = AbstractEmailForm.content_panels + [
        FieldPanel('body'),
        InlinePanel('form_fields', label="Form fields"),
        FieldPanel('thank_you_text'),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('from_address', classname="col6", heading="From Email", help_text="Email address that will be used to send the email"),
                FieldPanel('to_address', classname="col6", heading="Admin Email", help_text="Admin email address to receive new registration notifications"),
            ]),
            FieldPanel('subject', help_text="Subject of the email that will be sent to new registrants"),
        ], "Email"),
    ]

    parent_page_types = ['newsletter.NewsletterPage']

    def render_email(self, form, **kwargs):
        if kwargs.get('email_template'):
            return render_to_string(kwargs['email_template'], {'form': form})
        else:
            return render_to_string('news/email_template.html', {'form': form})

    def send_admin_notification(self, form):
        """Send an email notification to the admin when a new registration is submitted"""
        
        # Email addresses are parsed from the admin (to_address) email field
        admin_addresses = [x.strip() for x in self.to_address.split(',')]

        # Construct the email subject based on provided form data and the current date
        submitted_date_str = date.today().strftime('%x')
        admin_subject = f"Newsletter Registration: {form.cleaned_data['name']} ({form.cleaned_data['email']}) - {submitted_date_str}"\
        
        # Render the email's contents using the provided template
        admin_message = self.render_email(form, email_template='newsletter/admin_email_template.html')
        admin_plain_message = strip_tags(admin_message)

        send_mail(admin_subject, admin_plain_message, admin_addresses, 'Newsletter Registration<newsletter-registration@alanbridgeman.ca>', html_message=admin_message)
    
    def register_to_mailchimp(self, form):
        """Register a new subscriber to Mailchimp Marketing

        Args:
            form (_type_): The data submitted from the form
        """
        try:
            mailchimp = Client()
            mailchimp.set_config({
                "api_key": settings.MAILCHIMP_API_KEY,
                "server": settings.MAILCHIMP_REGION,
            })
            member_info = {
                'email_address': form.cleaned_data['email'],
                'status': 'subscribed',
                'merge_fields': {
                    'FNAME': form.cleaned_data['name'],
                    #'LNAME': form.cleaned_data['name']
                }
            }
            response = mailchimp.lists.add_list_member(
                settings.MAILCHIMP_MARKETING_AUDIENCE_ID, 
                member_info
            )
            print(f'API call successful: {response}')
        except ApiClientError as error:
            print("An exception occurred: {}".format(error.text))
    
    def send_subscriber_notification(self, form):
        """Send an email notification to the subscriber upon successful registration"""

        # Email addresses are parsed from the emails provided through the form
        signup_addresses = [x.strip() for x in form.cleaned_data['email'].split(',')]

        # Render the email's contents using the provided template
        subscriber_message = self.render_email(form, email_template='newsletter/subscriber_email_template.html')
        subscriber_plain_message = strip_tags(subscriber_message)

        send_mail(self.subject, subscriber_plain_message, signup_addresses, "Newsletter<newsletter@alanbridgeman.ca>", html_message=subscriber_message)

    def send_mail(self, form):
        """Override the AbstractEmailForm's default send_mail method to send an email to the admin and the subscriber as well as register the subscriber to Mailchimp if appropriate"""

        if self.to_address:
            self.send_admin_notification

        if self.auto_register_to_mailchimp:
            self.register_to_mailchimp(form)

        self.send_subscriber_notification(form)