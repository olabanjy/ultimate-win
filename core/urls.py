from django.urls import path, include
from .views import *
from django.contrib.auth.decorators import login_required

app_name = "core"


urlpatterns = [
    path("", Homepage.as_view(), name="home"),
    path("complete_payment/", complete_payment, name="complete_payment"),
]
