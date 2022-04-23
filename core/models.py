from datetime import datetime
from xml.parsers.expat import model
from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils import timezone
from uuid import uuid4


class Player(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid4, editable=False)
    full_name = models.CharField(max_length=200, blank=True, null=True)
    email = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)
    city = models.CharField(max_length=200, blank=True, null=True)
    ticket_sales = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email


class TicketSale(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid4, editable=False)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    ref_code = models.CharField(max_length=30000, null=True)
    payment_mode = models.CharField(max_length=50)
    paid = models.BooleanField(default=False)
    ticket_number = models.CharField(max_length=200, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.player
