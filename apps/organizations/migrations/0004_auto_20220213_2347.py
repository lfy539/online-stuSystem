# Generated by Django 3.2 on 2022-02-13 23:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0003_remove_citydict_add_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='courseorg',
            name='is_auth',
            field=models.BooleanField(default=False, verbose_name='是否认证'),
        ),
        migrations.AddField(
            model_name='courseorg',
            name='is_gold',
            field=models.BooleanField(default=False, verbose_name='是否金牌'),
        ),
    ]
