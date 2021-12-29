# Generated by Django 3.2.5 on 2021-12-25 19:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('reciept', '0007_group_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='reciept',
            name='owner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='auth.user'),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='ItemInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=9)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reciept.item')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='item',
            name='payer',
            field=models.ManyToManyField(through='reciept.ItemInfo', to=settings.AUTH_USER_MODEL),
        ),
    ]
