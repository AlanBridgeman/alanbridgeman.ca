from wagtail import blocks

class Podcast(blocks.StructBlock):
    title = blocks.CharBlock(max_length=255, help_text="Title of the podcast")
    description = blocks.RichTextBlock(classname="full", help_text="Description of the podcast and particularly why it's relevant to the topic")
    link = blocks.URLBlock(max_length=255, help_text="Link to the podcast")

    class Meta:
        verbose_name = "Podcast"
        verbose_name_plural = "Podcasts"