# Generated by Django 2.2.15 on 2020-09-18 22:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('todoes', '0007_auto_20200912_2254'),
    ]

    operations = [
        migrations.CreateModel(
            name='TodoProxy',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('todoes.todo',),
        ),
        migrations.RemoveField(
            model_name='repeatabletodo',
            name='history',
        ),
        migrations.RemoveField(
            model_name='todo',
            name='until',
        ),
        migrations.AddField(
            model_name='repeatabletodo',
            name='clocked_schedule',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='todoes.ClockedTODOSchedule'),
        ),
        migrations.AddField(
            model_name='repeatabletodohistory',
            name='task',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='todoes.TODO'),
            preserve_default=False,
        ),
    ]
