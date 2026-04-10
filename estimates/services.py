from jobs.models import Job


def accept_estimate(estimate):
    if estimate.status == 'accepted' and hasattr(estimate, 'job'):
        return estimate.job

    estimate.status = 'accepted'
    estimate.save()

    job, _ = Job.objects.get_or_create(
        estimate=estimate,
        defaults={
            'start_date': estimate.visit_date,
            'status': 'scheduled',
        },
    )
    return job
