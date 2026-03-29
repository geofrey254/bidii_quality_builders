from django.contrib import admin
from .models import Invoice

# Register your models here.


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('job', 'total_amount', 'issued_date', 'due_date', 'paid')
    list_filter = ('paid',)
    search_fields = ('job__estimate__customer__name',)
