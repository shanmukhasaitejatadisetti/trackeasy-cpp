from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime as d

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('in_transit', 'In Transit'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    
    VEHICLE_CHOICES = [
        ('small_van', 'Small Van'),
        ('box_truck', 'Box Truck'),
        ('refrigerated_truck', 'Refrigerated Truck'),
        ('motor_cycle', 'Motor Cycle'),
        ('cargo_van', 'Cargo Van'),
        ('dump_truck', 'Dump Truck'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    destination = models.CharField(max_length=255)
    goods_type = models.CharField(max_length=255)
    assigned_vehicle = models.CharField(max_length=50, choices=VEHICLE_CHOICES, blank=True, null=True)
    driver_name = models.CharField(max_length=100, blank=True, null=True)
    driver_contact = models.CharField(max_length=20, blank=True, null=True)
    delivery_requirements = models.TextField(blank=True, null=True)
    preferred_delivery_date = models.DateField()
    # created_at = models.DateTimeField(default=timezone.now)
    created_at = models.CharField(default=d.timestamp(d.now()),max_length=25)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    image_url = models.URLField(max_length=255, blank=True, null=True)  # New field for S3 image URL

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Order {self.id} - {self.goods_type} to {self.destination}"
