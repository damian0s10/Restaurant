# Generated by Django 3.0.6 on 2020-05-17 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'Categories'},
        ),
        migrations.AddField(
            model_name='product',
            name='size',
            field=models.PositiveSmallIntegerField(choices=[(1, 'small size'), (2, 'big size')], default=2),
        ),
    ]