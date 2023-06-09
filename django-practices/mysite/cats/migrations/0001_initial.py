# Generated by Django 4.0.7 on 2023-04-01 15:30

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Breed',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Enter a breed (e.g. Scottish Fold)', max_length=200, validators=[django.core.validators.MinLengthValidator(2, 'Breed must be greater than 1 character')])),
            ],
        ),
        migrations.CreateModel(
            name='Cat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nickname', models.CharField(max_length=200, validators=[django.core.validators.MinLengthValidator(2, "Cat's name must be greater than 1 character")])),
                ('weight', models.PositiveIntegerField()),
                ('food', models.CharField(max_length=300)),
                ('breed', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cats.breed')),
            ],
        ),
    ]
