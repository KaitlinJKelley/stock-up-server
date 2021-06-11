# Generated by Django 3.2.4 on 2021-06-11 19:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stockupapi', '0008_auto_20210611_1541'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='part',
            options={'ordering': ['name']},
        ),
        migrations.AlterField(
            model_name='company',
            name='parts',
            field=models.ManyToManyField(related_name='companies', through='stockupapi.CompanyPart', to='stockupapi.Part'),
        ),
        migrations.AlterField(
            model_name='company',
            name='vendor',
            field=models.ManyToManyField(related_name='companies', to='stockupapi.Vendor'),
        ),
        migrations.AlterField(
            model_name='orderrec',
            name='products',
            field=models.ManyToManyField(related_name='order_recs', to='stockupapi.Product'),
        ),
        migrations.AlterField(
            model_name='product',
            name='parts',
            field=models.ManyToManyField(related_name='products', through='stockupapi.ProductPart', to='stockupapi.CompanyPart'),
        )
    ]