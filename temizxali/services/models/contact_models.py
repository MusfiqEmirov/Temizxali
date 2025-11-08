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
    phone_second = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name='Telefon ikinci'
    )
    email = models.EmailField(
        null=True,
        blank=True,
        verbose_name='Email'
    )
    email_second = models.EmailField(
        null=True,
        blank=True,
        verbose_name='Email ikinci'
    )
    social_one = models.URLField(
        null=True,
        blank=True,
        verbose_name='Sosial şəbəkə 1 urli'
    )
    social_two = models.URLField(
        null=True,
        blank=True,
        verbose_name='Sosial şəbəkə 2 urli'
    )
    social_three = models.URLField(
        null=True,
        blank=True,
        verbose_name='Sosial şəbəkə 3 urli'
    )

    class Meta:
        verbose_name = "Əlaqə"
        verbose_name_plural = "Əlaqələr"

    def __str__(self):
        return self.address