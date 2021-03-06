# Generated by Django 2.0.3 on 2018-05-19 11:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import markupfield.fields


class Migration(migrations.Migration):

    replaces = [
        ('guides', '0001_initial'),
        ('guides', '0002_change_content_to_markup_field'),
        ('guides', '0003_change_ordering_add_help_texts_apply_cascade'),
        ('guides', '0004_guide_editors'),
        ('guides', '0005_remove_guide_editors')
    ]

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Guide',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Give your guide a readable and descriptive title.', max_length=100)),
                ('overview', models.TextField(help_text='A short overview of the guide, used for preview information and in OGP tags.', max_length=200)),
                ('content', markupfield.fields.MarkupField(help_text='Markdown with fenced code blocks (GFM) is supported.', rendered_field=True)),
                ('pub_datetime', models.DateTimeField(auto_now_add=True)),
                ('edit_datetime', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('_content_rendered', models.TextField(default='', editable=False)),
                ('content_markup_type', models.CharField(choices=[('', '--'), ('markdown', 'markdown')], default='markdown', editable=False, max_length=30)),
            ],
            options={
                'ordering': ['-pub_datetime'],
            },
        ),
    ]
