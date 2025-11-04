from django.db import models


class Statistics(models.Model):
    client_count = models.IntegerField(
        null=True,
        blank=True,
        verbose_name='Client sayı',
    )
    work_done_count = models.IntegerField(
        null=True, 
        blank=True,
        verbose_name='Görülmüş iş sayı'
    )
    staff_count = models.IntegerField(
        null=True, 
        blank=True,
        verbose_name='İşçi sayı'
    )
    achievement_count = models.IntegerField(
        null=True, 
        blank=True,
        verbose_name='Nailiyyət sayı'
    )

    class Meta:
        verbose_name = "Statistika"
        verbose_name_plural = "Statistikalar"

    def __str__(self):
        return 'Statistika'