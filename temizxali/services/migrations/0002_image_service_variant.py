# Generated manually for adding service_variant ForeignKey to Image model

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='service_variant',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='images',
                to='services.servicevariant',
                verbose_name='Servis növü'
            ),
        ),
    ]

