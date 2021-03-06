# Generated by Django 3.2 on 2021-04-26 19:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0008_stockcheck'),
    ]

    operations = [
        migrations.CreateModel(
            name='Model',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Vendor Name')),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.vendor', verbose_name='Vendor')),
            ],
            options={
                'verbose_name': 'Model',
                'verbose_name_plural': 'Models',
            },
        ),
    ]
