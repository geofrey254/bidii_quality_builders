from django.shortcuts import get_object_or_404, redirect
from .models import Estimate
from .services import accept_estimate


def accept_estimate_view(request, pk):
    estimate = get_object_or_404(Estimate, pk=pk)
    accept_estimate(estimate)
    return redirect('estimate-list')
