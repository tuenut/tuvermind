# Generated by Django 2.2.15 on 2020-09-21 11:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('todoes', '0002_auto_20200921_1117'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='TODOHistory',
            new_name='TodoTaskHistory',
        ),
    ]