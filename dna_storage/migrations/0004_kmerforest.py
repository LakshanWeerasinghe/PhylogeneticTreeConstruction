# Generated by Django 2.2.10 on 2020-05-18 06:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dna_storage', '0003_delete_kmerforest'),
    ]

    operations = [
        migrations.CreateModel(
            name='KmerForest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(max_length=250)),
                ('kmer_count', models.IntegerField()),
                ('dna_file', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dna_storage.DNAFile')),
            ],
        ),
    ]
