# Generated by Django 4.1.7 on 2023-02-27 11:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0003_category_editors_books_description_books_language_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Editors',
            new_name='Editor',
        ),
        migrations.RenameField(
            model_name='books',
            old_name='editors',
            new_name='editor',
        ),
    ]
