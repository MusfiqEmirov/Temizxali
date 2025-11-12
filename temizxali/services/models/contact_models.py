from django.db import models


class Contact(models.Model):
    address = models.CharField(
        max_length=255,
        verbose_name='Ünvan'
    )
    phone = models.CharField(
        max_length=50,
        verbose_name='Telefon'
    )
    email = models.EmailField(
        null=True,
        blank=True,
        verbose_name='Email'
    )
    instagram = models.URLField(
        null=True,
        blank=True,
    )
    facebook = models.URLField(
        null=True,
        blank=True,
    )
    youtube = models.URLField(
        null=True,
        blank=True,
    )
    linkedn = models.URLField(
        null=True,
        blank=True,
    )
    tiktok = models.URLField(
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Əlaqə"
        verbose_name_plural = "Əlaqələr"

    def __str__(self):
        return self.address