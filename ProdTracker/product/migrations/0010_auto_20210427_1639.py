# Generated by Django 3.2 on 2021-04-27 16:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0009_model'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='model',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='product.model', verbose_name='Vendor'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='model',
            name='vendor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vendor', to='product.vendor', verbose_name='Vendor'),
        ),
        migrations.AlterUniqueTogether(
            name='product',
            unique_together={('model', 'serial_num')},
        ),
        migrations.RemoveField(
            model_name='product',
            name='model_no',
        ),
        migrations.RemoveField(
            model_name='product',
            name='vendor',
        ),
    ]