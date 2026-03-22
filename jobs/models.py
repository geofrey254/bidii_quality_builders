from django.db import models
from estimates.models import Estimate


class Job(models.Model):
    estimate = models.OneToOneField(Estimate, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(
        choices=[('scheduled', 'Scheduled'), ('ongoing',
                                              'Ongoing'), ('completed', 'Completed')],
        max_length=10
    )

    def __str__(self):
        return f"Job for Estimate {self.estimate.id} - Status: {self.status}"
