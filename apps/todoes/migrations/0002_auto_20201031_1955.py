# Generated by Django 2.2.15 on 2020-10-31 19:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todoes', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='todotaskreminder',
            old_name='remind_for_minutes',
            new_name='value',
        ),
        migrations.AddField(
            model_name='todotaskreminder',
            name='dimension',
            field=models.CharField(default='min', max_length=4),
        ),
    ]
