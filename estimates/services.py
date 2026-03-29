from jobs.models import Job


def accept_estimate(estimate):
    estimate.status = 'accepted'
    estimate.save()

    Job.objects.create(
        estimate=estimate,
        start_date=estimate.visit_date,
        status='scheduled'
    )
