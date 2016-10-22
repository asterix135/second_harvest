from django.conf.urls import url
from . import views

app_name = 'sales'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^client_info$', views.client_info, name='client_info'),
    url(r'^ticket_info$', views.ticket_info, name='ticket_info'),
    url(r'^thankyou$', views.thankyou, name='thankyou'),
    url(r'^welcome$', views.welcome, name='welcome')
]
