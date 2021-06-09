# Generated by Django 3.2.4 on 2021-06-09 19:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stockupapi', '0003_auto_20210609_1748'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='parts',
            field=models.ManyToManyField(related_name='company_parts', through='stockupapi.CompanyPart', to='stockupapi.Part'),
        ),
        migrations.AddField(
            model_name='company',
            name='vendor',
            field=models.ManyToManyField(related_name='companyvendor', to='stockupapi.Vendor'),
        ),
        migrations.AddField(
            model_name='orderrec',
            name='parts',
            field=models.ManyToManyField(through='stockupapi.OrderRecPart', to='stockupapi.ProductPart'),
        ),
        migrations.AddField(
            model_name='orderrec',
            name='products',
            field=models.ManyToManyField(related_name='OrderProduct', to='stockupapi.Product'),
        ),
        migrations.AddField(
            model_name='product',
            name='parts',
            field=models.ManyToManyField(related_name='product_part', through='stockupapi.ProductPart', to='stockupapi.CompanyPart'),
        ),
    ]
