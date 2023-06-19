# Generated by Django 4.1.7 on 2023-03-08 00:08

from django.db import migrations
import wagtail.blocks
import wagtail.contrib.table_block.blocks
import wagtail.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ("portfolio", "0004_remove_animation_raw_file_rawfiles"),
    ]

    operations = [
        migrations.AddField(
            model_name="creativeportfoliopage",
            name="body",
            field=wagtail.fields.StreamField(
                [
                    ("heading", wagtail.blocks.CharBlock(form_classname="title")),
                    ("paragraph", wagtail.blocks.RichTextBlock()),
                    ("image", wagtail.images.blocks.ImageChooserBlock()),
                    ("table", wagtail.contrib.table_block.blocks.TableBlock()),
                ],
                blank=True,
                use_json_field=True,
            ),
        ),
    ]