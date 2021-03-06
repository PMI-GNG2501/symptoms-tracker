# Generated by Django 3.2.7 on 2021-10-15 21:49

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('therapies', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='therapies',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='therapies',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='therapies',
            name='comments',
            field=models.TextField(blank=True),
        ),
    ]
