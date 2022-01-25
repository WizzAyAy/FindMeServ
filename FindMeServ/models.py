from django.utils.translation import gettext_lazy as _
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


class Server(models.Model):
    class ServerType(models.TextChoices):
        RETAKE = 'RT', _('Retake')
        DEATHMATCH = 'DM', _('Deathmatch')
        EXECUTE = 'EX', _('Execute')
        SURF = 'SU', _('Surf')
        KZ = 'KZ', _('Kz')
        OTHER = 'OT', _('Other')

    ip = models.CharField(max_length=30, null=False)
    port = models.IntegerField(null=False)
    host = models.CharField(max_length=30, null=False)

    gamemode = models.CharField(
        max_length=2,
        choices=ServerType.choices,
        default=ServerType.OTHER,
    )

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    class Meta:
        unique_together = ("ip", "port",)

    def get_ip(self):
        return self.ip

    def get_port(self):
        return self.port

    def get_host(self):
        return self.host

    def get_gamemode(self):
        return self.gamemode

    def get_owner(self):
        return User.objects.get(id=self.owner)

    def get_id(self):
        return self.id
