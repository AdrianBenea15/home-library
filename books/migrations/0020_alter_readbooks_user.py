# Generated by Django 4.1.7 on 2023-03-06 11:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0019_remove_readbooks_author_remove_readbooks_category_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='readbooks',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
