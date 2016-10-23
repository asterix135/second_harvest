from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout

from .forms import *
from .models import *
from django.contrib.auth.models import User
from .constants import DEFAULT_PRICES


def login_site(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                request.session['seller'] = request.user.id
                #######
                # Need to Update this
                #######
                request.session['campaign'] = 1

                return HttpResponseRedirect(reverse('sales:welcome'))
    return render(request, 'sales/login.html')


def logout_site(request):
    del request.session['seller']
    del request.session['campaign']
    logout(request)
    return HttpResponseRedirect(reverse('sales:login_site'))


##################
# helper fn
##################
def ticket_is_new(ticket_number):
    if Tickets.objects.filter(tick_id=ticket_number).exists():
        print('\n\n\nOMG!!!!\n\n')
        return False
    else:
        return True

def ticket_info(request):
    ##########
    # Delete when code is complete
    ##########
    if 'seller' not in request.session:
        request.session['seller'] = 1
    if 'buyer' not in request.session:
        request.session['buyer'] = 1
    if 'campaign' not in request.session:
        request.session['campaign'] = 1
    #############
    # end delete section
    #############
    curr_campaign = Campaign.objects.get(pk=request.session['campaign'])
    prices = {
        'price1': curr_campaign.tick_price1,
        'price3': curr_campaign.tick_price3,
        'price10': curr_campaign.tick_price10
    }
    context = {'price1': prices['price1'],
               'price3': prices['price3'],
               'price10': prices['price10']}
    if request.method == 'POST':
        ticket_prices = {}
        tickets = {}
        for key in request.POST:
            if key[:8] == 'selector':
                ticket_prices[key[8:]] = request.POST[key]
            elif key[:6] == 'ticket':
                tickets[key[6:]] = request.POST[key]
        new_tickets = []
        total_price = 0
        for key in tickets:
            if not ticket_is_new(tickets[key]):
                # raise error and return to ticket info page
                context['multi_key_error'] = "Ticket number " + \
                    str(tickets[key]) + \
                    ' has already been sold.  Please check your entry.'
                return render(request, 'sales/ticket_info.html', context)
            price_lookup = ticket_prices[key[:len(key)-2]]
            if str(price_lookup) in ['1', '2']:
                new_tickets.append(Tickets(
                    tick_id = str(tickets[key]),
                    sale_date = timezone.now(),
                    tick_type = price_lookup,
                    buyer_id = Buyer.objects.get(pk=request.session['buyer']),
                    seller_id = request.user,
                    camp_id = Campaign.objects.get(pk=request.session['campaign'])
                ))
                total_price += prices['price1'] if str(price_lookup) == '1' \
                    else prices['price3'] / 3
            else:
                for i in range(10):
                    new_tickets.append(Tickets(
                        tick_id = str(int(tickets[key]) + i),
                        sale_date = timezone.now(),
                        tick_type = price_lookup,
                        buyer_id = Buyer.objects.get(pk=request.session['buyer']),
                        seller_id = request.user,
                        camp_id = Campaign.objects.get(pk=request.session['campaign'])
                    ))
                total_price += prices['price10']
        for ticket in new_tickets:
            ticket.save()
        request.session['total_price'] = str(total_price)
        return HttpResponseRedirect(reverse('sales:thankyou'))

    return render(request, 'sales/ticket_info.html', context)


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


def thankyou(request):
    if request.method == 'POST':
        del request.session['buyer']
        del request.session['total_price']
        return HttpResponseRedirect(reverse('sales:welcome'))
    context = {
        'ticket_cost': request.session['total_price']
    }
    return render(request, 'sales/thankyou.html', context)


def welcome(request):

    ##########
    # Delete when code is complete
    ##########
    if 'seller' not in request.session:
        request.session['seller'] = 1
    if 'buyer' not in request.session:
        request.session['buyer'] = 1
    if 'campaign' not in request.session:
        request.session['campaign'] = 1
    #############
    # end delete section
    #############

    if request.method == 'POST':
        return HttpResponseRedirect(reverse('sales:client_info'))
    seller = User.objects.get(pk=request.session['seller'])
    tickets_sold = Tickets.objects.filter(seller_id_id=request.session['seller']).count()

    money_sold_singles = Tickets.objects.filter(
        seller_id_id=request.session['seller'],
        tick_type=1,
        camp_id_id=request.session['campaign']
    ).count() * Campaign.objects.get(pk=request.session['campaign']).tick_price1
    money_sold_triples = Tickets.objects.filter(
        seller_id_id=request.session['seller'],
        tick_type=2,
        camp_id_id=request.session['campaign']
    ).count() * Campaign.objects.get(pk=request.session['campaign']).tick_price3 / 3
    money_sold_tens = Tickets.objects.filter(
        seller_id_id=request.session['seller'],
        tick_type=3,
        camp_id_id=request.session['campaign']
    ).count() * Campaign.objects.get(pk=request.session['campaign']).tick_price10 / 10

    total_sold_singles = Tickets.objects.filter(
        tick_type=1,
        camp_id_id=request.session['campaign']
    ).count() * Campaign.objects.get(pk=request.session['campaign']).tick_price1
    total_sold_triples = Tickets.objects.filter(
        tick_type=2,
        camp_id_id=request.session['campaign']
    ).count() * Campaign.objects.get(pk=request.session['campaign']).tick_price3 / 3
    total_sold_tens = Tickets.objects.filter(
        tick_type=3,
        camp_id_id=request.session['campaign']
    ).count() * Campaign.objects.get(pk=request.session['campaign']).tick_price10 / 10
    total_raised = total_sold_singles + total_sold_triples + total_sold_tens


    campaign_goal = Campaign.objects.get(pk=request.session['campaign']).fund_goal
    therm_url = 'http://www.coolfundraisingideas.net/thermometer/thermometer.php?currency=dollar&goal=' + \
        str(campaign_goal) + '&current=' + str(total_raised) + \
        '&color=green&size=large'
    context = {
        'seller_name': seller.first_name,
        'tickets_sold': tickets_sold,
        'money_sold': money_sold_singles + money_sold_triples + money_sold_tens,
        'campaign_goal': "{:,}".format(campaign_goal),
        'image_src': therm_url,
    }
    return render(request, 'sales/welcome.html', context)
