from django.db import models
from customer.models import Customer


class Estimate(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    description = models.TextField()
    visit_date = models.DateField()
    estimated_cost = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        choices=[('pending', 'Pending'), ('accepted', 'Accepted'),
                 ('rejected', 'Rejected')],
        max_length=10
    )

    def __str__(self):
        return f"Estimate for {self.customer.name} - Status: {self.status}"
