# Generated by Django 2.2.6 on 2019-10-20 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fashion_catalogue', '0015_reviews'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reviews',
            name='published',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
