# Generated by Django 3.1.4 on 2020-12-14 16:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='art_id',
            new_name='art',
        ),
    ]
