from django.urls import path
from .views import index, giver, send_friend, form, presents, receiver, giver_self


urlpatterns = [
    path("", index),
    path("giver/", giver, name="giver"),
    path("giver-self/", giver_self, name="giver-self"),
    path("receiver/", receiver, name="receiver"),
    path("send-friend/", send_friend, name="send-friend"),
    path("form/<uuid:form_uuid>/", form, name="form"),
    path("presents/<uuid:form_uuid>/", presents, name="presents"),
]
