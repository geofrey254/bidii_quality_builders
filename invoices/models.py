from django.db import models
from jobs.models import Job


class Invoice(models.Model):
    job = models.OneToOneField(Job, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    issued_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Invoice for Job {self.job.id} - Paid: {self.paid}"
