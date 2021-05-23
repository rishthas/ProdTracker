# Generated by Django 3.2 on 2021-05-17 17:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0010_auto_20210427_1639'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='pur_invoce_no',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Purchase Invoice Number'),
        ),
        migrations.AlterField(
            model_name='product',
            name='model',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.model', verbose_name='Model'),
        ),
    ]