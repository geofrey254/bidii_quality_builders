from django.contrib import admin
from .models import Estimate

# Register your models here.


@admin.register(Estimate)
class EstimateAdmin(admin.ModelAdmin):
    list_display = ('customer', 'description', 'visit_date',
                    'estimated_cost', 'status')
    list_filter = ('status',)
    search_fields = ('customer__name', 'description')
