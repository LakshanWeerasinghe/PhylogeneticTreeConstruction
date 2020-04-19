# Generated by Django 2.2.10 on 2020-04-19 20:09

from django.conf import settings
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dna_storage', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Process',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('type', models.IntegerField(choices=[(1, 'MATRIX_GENERATION'), (2, 'TREE_GENERATION')])),
                ('method', models.IntegerField(choices=[(1, 'LSH'), (2, 'K_MEDOID_LSH_CLUSTER'), (3, 'K_MER'), (4, 'K_MEDOID_K_MER_CLUSTER')])),
                ('status', models.IntegerField(choices=[(1, 'PROGRESS'), (2, 'SUCCESS')])),
                ('crated_at', models.DateTimeField(auto_now_add=True)),
                ('dna_files', models.ManyToManyField(to='dna_storage.DNAFile')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TreeResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tree', django.contrib.postgres.fields.jsonb.JSONField()),
                ('process', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cluster.Process')),
            ],
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('result', models.TextField()),
                ('process', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cluster.Process')),
            ],
        ),
    ]
