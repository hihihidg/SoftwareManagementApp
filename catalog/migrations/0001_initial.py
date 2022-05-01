# Generated by Django 4.0.4 on 2022-04-29 01:51

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Software',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300)),
                ('description', models.TextField(help_text='Enter a description of the software', max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='SoftwareType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Enter the type of software', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='SoftwareInstance',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, help_text='Unique ID for this software instance', primary_key=True, serialize=False)),
                ('renewal_date', models.DateField(blank=True, null=True)),
                ('status', models.CharField(blank=True, choices=[('i', 'In Use'), ('u', 'Unavailable'), ('a', 'Available')], default='a', help_text='Software Status', max_length=1)),
                ('software', models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to='catalog.software')),
            ],
            options={
                'ordering': ['renewal_date'],
            },
        ),
        migrations.AddField(
            model_name='software',
            name='softwaretype',
            field=models.ManyToManyField(help_text='Select software types', to='catalog.softwaretype'),
        ),
    ]
