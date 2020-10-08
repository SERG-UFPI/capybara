# Generated by Django 3.1.1 on 2020-09-16 20:27

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_auto_20200916_2027'),
    ]

    operations = [
        migrations.AddField(
            model_name='issue',
            name='comments',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.JSONField(blank=True, null=True), blank=True, null=True, size=None),
        ),
        migrations.AddField(
            model_name='pullrequest',
            name='comments',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.JSONField(blank=True, null=True), blank=True, null=True, size=None),
        ),
    ]