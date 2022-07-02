from django.db import models
from django.utils.translation import gettext_lazy as _


class Client(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name=_('Name'))

    def __str__(self):
        return self.name


class Organization(models.Model):
    client_name = models.CharField(max_length=255, unique=True, verbose_name=_('Client name'))
    name = models.CharField(max_length=255, unique=True, verbose_name=_('Name'))
    address = models.CharField(max_length=255, unique=True, verbose_name=_('Address'), blank=True)

    def __str__(self):
        return f"{self.client_name}: {self.name}"


class Bill(models.Model):
    client_name = models.CharField(max_length=255, verbose_name=_('Client name'))
    client_org = models.CharField(max_length=255, unique=True, verbose_name=_('Client organization'))
    number = models.PositiveSmallIntegerField(unique=True)
    amount = models.CharField(max_length=10, verbose_name=_('Sum'))
    date = models.DateTimeField()
    service = models.CharField(max_length=255)

    fraud_score = models.FloatField(verbose_name=_('Fraud detector score'))
    service_class = models.PositiveSmallIntegerField()
    service_name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.number}"
