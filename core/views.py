from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View
from django.views.defaults import page_not_found
from .models import TicketSale, Player
from django.conf import settings
import random, string
from django.http.response import JsonResponse

import requests
import json

# Create your views here.


# def error404(request, exception):
#     return page_not_found(request, exception, "errors/404.html")


# def error500(request):
#     return render(request, "errors/500.html")


def is_unique(ticket_number):
    try:
        TicketSale.objects.get(ticket_number=ticket_number)
    except TicketSale.DoesNotExist:
        return True
    return False


class Homepage(View):
    def get(self, request):
        template = "core/index.html"

        context = {"ticket_amount": 5000}

        return render(self.request, template, context)

    def post(self, request):
        pass


def complete_payment(request):
    data = json.loads(request.body)

    reference = data["reference"]
    fullname = data["fullname"]
    email = data["email"]
    phone = data["phone"]
    city = data["city"]

    headers = {"Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}"}
    resp = requests.get(
        f"https://api.paystack.co/transaction/verify/{reference}", headers=headers
    )
    response = resp.json()

    try:
        status = response["data"]["status"]
        if status == "success":
            new_player, created = Player.objects.get_or_create(
                email=email,
            )
            new_player.full_name = fullname
            new_player.phone = phone
            new_player.city = city

            new_player.save()

            new_sale = TicketSale(
                player=new_player,
                ref_code=reference,
                payment_mode="paystack",
                paid=True,
            )

            new_ticket_numb = str(
                "".join(random.choices(string.ascii_uppercase + string.digits, k=8))
            )
            if is_unique(new_ticket_numb):
                new_sale.ticket_number = new_ticket_numb

            new_sale.save()

            # send an email to user

            return JsonResponse(
                data={"status": "success", "ticket_number": new_sale.ticket_number},
            )
        else:
            print("payment not successful")
            return JsonResponse(
                data={"status": "failed"},
            )
    except Exception as e:
        print("there was an error")
        return JsonResponse(
            data={"status": "failed"},
        )
