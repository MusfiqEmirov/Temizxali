# Generated manually for adding whatsapp_number_2 field to Contact model

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0002_image_service_variant'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='whatsapp_number_2',
            field=models.CharField(
                blank=True,
                max_length=50,
                null=True,
                verbose_name='Whatsapp əlaqə nömrəsi 2'
            ),
        ),
    ]

