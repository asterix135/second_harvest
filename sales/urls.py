from django.conf.urls import url
from . import views

app_name = 'sales'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^client_info$', views.client_info),
    url(r'^ticket_info$', views.ticket_info),
    url(r'^thank_you$', views.thank_you),
]
