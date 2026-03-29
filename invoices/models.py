from django.db import models
from jobs.models import Job
from datetime import timedelta
from django.utils.timezone import now


class Invoice(models.Model):
    job = models.OneToOneField(Job, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    issued_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    paid = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.due_date:
            self.due_date = now().date() + timedelta(days=30)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Invoice for {self.job}"
