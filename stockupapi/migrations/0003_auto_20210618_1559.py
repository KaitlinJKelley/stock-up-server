# Generated by Django 3.2.4 on 2021-06-18 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stockupapi', '0002_rename_received_date_orderrecpart_date_received'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderrec',
            name='sales_end_date',
            field=models.DateTimeField(default=None, null=True),
        ),
        migrations.AddField(
            model_name='orderrec',
            name='sales_start_date',
            field=models.DateTimeField(default=None, null=True),
        ),
    ]
