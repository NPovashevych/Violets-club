# Generated by Django 5.0.1 on 2024-02-05 22:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('club', '0006_alter_status_options_alter_variety_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='status',
            options={'ordering': ('name',), 'verbose_name_plural': 'statuses'},
        ),
        migrations.AlterModelOptions(
            name='variety',
            options={'ordering': ('flower',), 'verbose_name_plural': 'varieties'},
        ),
    ]
