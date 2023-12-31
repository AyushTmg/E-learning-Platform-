# Generated by Django 5.0 on 2023-12-19 11:17

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='enrollment',
            name='id',
            field=models.BigAutoField(auto_created=True, default=1, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='content',
            name='files',
            field=models.FileField(blank=True, null=True, upload_to='content-file/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf', 'docx'])]),
        ),
        migrations.AlterField(
            model_name='enrollment',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='enrollment', to='core.course'),
        ),
    ]
