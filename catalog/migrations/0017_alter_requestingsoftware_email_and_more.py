# Generated by Django 4.0.4 on 2022-04-30 23:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0016_softwareinstance_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requestingsoftware',
            name='email',
            field=models.EmailField(max_length=300),
        ),
        migrations.AlterField(
            model_name='softwareinstance',
            name='status',
            field=models.CharField(blank=True, choices=[('a', 'Available'), ('u', 'Unailable')], default='a', help_text='Software Availability', max_length=1),
        ),
    ]
