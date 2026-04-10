from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView
from django.contrib import messages
from .models import Job


class JobListView(ListView):
    model = Job
    template_name = 'jobs/list.html'
    context_object_name = 'jobs'


def update_job_status(request, pk):
    if request.method != 'POST':
        return redirect('job-list')

    job = get_object_or_404(Job, pk=pk)
    new_status = request.POST.get('status')
    valid_statuses = {'scheduled', 'ongoing', 'completed'}

    if not new_status:
        messages.error(request, 'Status is required.')
        return redirect('job-list')

    if new_status not in valid_statuses:
        messages.error(request, 'Invalid status value.')
        return redirect('job-list')

    old_status = job.status
    job.status = new_status
    job.save(update_fields=['status'])
    messages.success(
        request, f'Job updated from {old_status} to {new_status}.')
    return redirect('job-list')
