from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404, redirect

from .forms import *

# Create your views here.
def index(request):
    return render(request, 'sales/index.html')


def ticket_info(request):
    if request.method == 'POST':
        pass
    return render(request, 'sales/ticket_info.html')


def client_info(request):
    if request.method == 'POST':
        form = DonorInputForm(request.POST)
        if form.is_valid():
            buyer = Buyer(
                first_name=request.POST['first_name'],
                last_name=request.POST['last_name'],
                email=request.POST['email'],
                phone=request.POST['phone'],
                address=request.POST['address'],
                city=request.POST['city'],
                postal_code=request.POST['postal_code'],
                opt_out=True if 'opt_out' in request.POST else False,
            )
            buyer.save()
            request.session['buyer'] = buyer.id
        return HttpResponseRedirect(reverse('sales:ticket_info'))
    context = {
        'buyer_form': DonorInputForm
    }
    return render(request, 'sales/client_info.html', context)


def thank_you(request):
    return render(request, 'sales/thank_you.html')
