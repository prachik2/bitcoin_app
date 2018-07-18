# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class GenerateAddress(models.Model):
    bitcoin_address = models.CharField(max_length=256)
    public_key_address = models.CharField(max_length=256)
    private_key_address = models.CharField(max_length=256)

    def __str__(self):
        return self.bitcoin_address

    def save(self, *args, **kwargs):
        super(GenerateAddress, self).save(*args, **kwargs)


class TransferAmount(models.Model):
    from_address = models.CharField(max_length=256)
    to_address = models.CharField(max_length=256)
    amount_field = models.IntegerField()