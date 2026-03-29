import matplotlib.pyplot as plt
from django.http import HttpResponse
import io
from invoices.models import Invoice


def revenue_chart(request):
    invoices = Invoice.objects.filter(paid=True)

    amounts = [float(i.total_amount) for i in invoices]

    plt.figure()
    plt.plot(amounts)

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    return HttpResponse(buffer.getvalue(), content_type='image/png')
