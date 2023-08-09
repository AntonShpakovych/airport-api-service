from django.contrib import admin

from cart.models import Order, Ticket


admin.site.register(Order)
admin.site.register(Ticket)
