# Generated by Django 2.2.10 on 2020-04-27 17:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cluster', '0002_auto_20200427_1416'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='result',
            name='process',
        ),
        migrations.RemoveField(
            model_name='treeresult',
            name='process',
        ),
        migrations.DeleteModel(
            name='Process',
        ),
        migrations.DeleteModel(
            name='Result',
        ),
        migrations.DeleteModel(
            name='TreeResult',
        ),
    ]
