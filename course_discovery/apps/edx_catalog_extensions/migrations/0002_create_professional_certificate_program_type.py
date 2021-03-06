# -*- coding: utf-8 -*-
# Generated by Django 1.9.11 on 2016-12-19 19:51
from __future__ import unicode_literals

from django.db import migrations

PAID_SEAT_TYPES = ('credit', 'professional', 'verified',)
PROGRAM_TYPE = 'Professional Certificate'


def add_program_type(apps, schema_editor):
    SeatType = apps.get_model('course_metadata', 'SeatType')
    ProgramType = apps.get_model('course_metadata', 'ProgramType')

    seat_types = SeatType.objects.filter(slug__in=PAID_SEAT_TYPES)

    program_type, __ = ProgramType.objects.update_or_create(name=PROGRAM_TYPE)
    program_type.applicable_seat_types.clear()
    program_type.applicable_seat_types.add(*seat_types)
    program_type.save()


def drop_program_type(apps, schema_editor):
    ProgramType = apps.get_model('course_metadata', 'ProgramType')
    ProgramType.objects.filter(name=PROGRAM_TYPE).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('edx_catalog_extensions', '0001_squashed_0003_create_publish_to_marketing_site_flag'),
    ]

    operations = [
        migrations.RunPython(add_program_type, drop_program_type)
    ]
