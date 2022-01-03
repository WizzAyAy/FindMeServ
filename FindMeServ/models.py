from django.utils.translation import gettext_lazy as _
from django.db import models


class Server(models.Model):
    class ServerType(models.TextChoices):
        RETAKE = 'RT', _('Retake')
        DEATHMATCH = 'DM', _('Deathmatch')
        EXECUTE = 'EX', _('Execute')
        SURF = 'SU', _('Surf')
        KZ = 'KZ', _('Kz')
        OTHER = 'OT', _('Other')

    ip = models.CharField(max_length=30)
    port = models.CharField(max_length=10)
    host = models.CharField(max_length=30)

    gamemode = models.CharField(
        max_length=2,
        choices=ServerType.choices,
        default=ServerType.OTHER,
    )

