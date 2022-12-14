# Generated by Django 4.1 on 2022-10-31 16:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0010_listing_winner'),
    ]

    operations = [
        migrations.CreateModel(
            name='Watch_list',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('list_watch', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='list_watch', to='auctions.listing')),
                ('user_watch_list', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_watch_list', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
