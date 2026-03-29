from django.contrib import admin
from .models import Job

# Register your models here.


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('estimate', 'start_date', 'end_date', 'status')
    list_filter = ('status',)
    search_fields = ('estimate__customer__name',)
