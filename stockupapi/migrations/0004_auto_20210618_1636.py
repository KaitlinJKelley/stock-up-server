# Generated by Django 3.2.4 on 2021-06-18 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stockupapi', '0003_auto_20210618_1559'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderrec',
            name='sales_end_date',
            field=models.DateField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='orderrec',
            name='sales_start_date',
            field=models.DateField(default=None, null=True),
        ),
    ]
