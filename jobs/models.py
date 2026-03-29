from django.db import models
from estimates.models import Estimate


class Job(models.Model):
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
    ]

    estimate = models.OneToOneField(Estimate, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='scheduled')

    def __str__(self):
        return f"Job for {self.estimate.customer.name}"
