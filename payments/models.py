from django.db import models
from orders.models import Order


class Payment(models.Model):
    PAYMENT_CHOICES = (
        ('cash', 'Cash'),
        ('aba', 'ABA'),
        ('bakong', 'Bakong'),
        ('card', 'Card'),
    )

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
    )

    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    paid_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.payment_method} - {self.status}"