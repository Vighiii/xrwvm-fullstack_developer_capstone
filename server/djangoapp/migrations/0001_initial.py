import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CarMake',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID'
                    )
                ),
                ('name', models.CharField(max_length=150, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='CarModel',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID'
                    )
                ),
                ('dealer_id', models.IntegerField()),
                ('name', models.CharField(max_length=150)),
                (
                    'type',
                    models.CharField(
                        choices=[
                            ('Sedan', 'Sedan'),
                            ('SUV', 'SUV'),
                            ('Wagon', 'Wagon')
                        ],
                        default='Sedan',
                        max_length=10
                    )
                ),
                (
                    'year',
                    models.IntegerField(
                        default=2020,
                        validators=[
                            django.core.validators.MaxValueValidator(2023),
                            django.core.validators.MinValueValidator(2015)
                        ]
                    )
                ),
                (
                    'car_make',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to='djangoapp.carmake'
                    )
                ),
            ],
            options={
                'unique_together': {('car_make', 'name')},
            },
        ),
    ]
