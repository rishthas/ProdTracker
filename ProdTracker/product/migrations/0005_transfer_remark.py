# Generated by Django 3.2 on 2021-04-08 21:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_alter_product_unique_together'),
    ]

    operations = [
        migrations.AddField(
            model_name='transfer',
            name='remark',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Remarks'),
        ),
    ]
