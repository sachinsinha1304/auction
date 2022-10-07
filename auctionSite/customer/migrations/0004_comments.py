# Generated by Django 4.0.6 on 2022-10-04 06:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0003_alter_item_closingdate_alter_userdetails_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField()),
                ('rating', models.IntegerField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer.item')),
            ],
        ),
    ]
