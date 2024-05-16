from django.shortcuts import render
from .models import Header, AboutUs, PaymentDelivery, Safeguards, ReturnAgoods




def about_us(request):
    informations = AboutUs.objects.all()
    return render(request, 'main/about_us.html', {'informations': informations})


def payment_delivery(request):
    informations = PaymentDelivery.objects.all()
    return render(request, 'main/payment_delivery.html', {'informations': informations})


def safeguards(request):
    informations = Safeguards.objects.all()
    return render(request, 'main/safeguards.html', {'informations': informations})

def return_a_goods(request):
    informations = ReturnAgoods.objects.all()
    return render(request, 'main/return_a_goods.html', {'informations': informations})
