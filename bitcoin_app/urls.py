from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'generate-address/', views.generate_address, name='generate_address'),
    url(r'list-transactions/', views.list_transactions, name='list_transactions'),
    url(r'transfer-amount/', views.transfer_amount, name='transfer_amount'),
    url(r'private-key-address/(?P<bitcoin_address>([A-Z1-9a-z]{35}))+/', views.private_key_address, name='private_key_address'),
    url(r'public-key-address/(?P<bitcoin_address>([A-Z1-9a-z]{35}))+/', views.public_key_address, name='public_key_address'),
    url(r'hello/', views.hello, name='hello'),
]
