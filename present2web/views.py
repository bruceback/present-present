from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from .models import Question, TempUrl, Present, Category
from django.contrib.sites.shortcuts import get_current_site
import json
import requests


def types_qstn():
    if getattr(types_qstn, "__types", None) is None:
        types_qstn.__types = {q.priority: q.type_answer for q in Question.objects.all()}
    return types_qstn.__types


def index(request):
    request.session["is_giver"] = False
    request.session["is_receiver"] = False
    return render(request, "index.html")


def giver(request):
    return render(request, "giver.html")


def send_friend(request):
    url_to_friend = TempUrl.objects.create().questionnaire_uuid
    ctx = {"url_to_friend": request.build_absolute_uri(f"/form/{url_to_friend}/")}
    return render(request, "send_friend.html", ctx)


@csrf_exempt
def form(request, form_uuid):
    if request.method == "GET":
        if not request.session.get("is_giver"):
            request.session["is_receiver"] = True
        ctx = {"questions": Question.objects.all(), "form_uuid": form_uuid}
        response = render(request, "form.html", ctx)
        return response
    else:
        types = types_qstn()
        data = dict()
        for key, value in request.POST.items():
            lst = request.POST.getlist(key)
            if key != "button":
                if types[int(key)] in [2, 3]:
                    data[key] = lst
                else:
                    data[key] = value
        temp_url = TempUrl.objects.get(questionnaire_uuid=form_uuid)

        try:
            r = requests.post("https://b38bb539dbeb.ngrok.io/predict", json=data)
            r = r.json()
        except Exception:
            return render(request, "error.html")
        if r["code"] == 0:
            temp_url.category = Category.objects.get(pk=(r["class"] + 1))
            temp_url.rules = r["rules"].lower()
        else:
            return render(request, "error.html")
        temp_url.save()
        ctx = {
            "url_to_friend": request.build_absolute_uri(
                f"/presents/{temp_url.presents_uuid}/"
            )
        }
        if request.session.get("is_giver"):
            return redirect("presents", form_uuid=temp_url.presents_uuid)
        return render(request, "send_friend.html", ctx)


def presents(request, form_uuid):
    if request.session.get("is_receiver"):
        return render(request, "unavailable.html")
    temp_url = TempUrl.objects.get(presents_uuid=form_uuid)
    presents_2000 = Present.objects.filter(
        category=temp_url.category, price__lte=2000
    ).order_by("?")[:4]
    presents_2001_5000 = Present.objects.filter(
        category=temp_url.category, price__gt=2000, price__lte=5000
    ).order_by("?")[:4]
    presents_5000 = Present.objects.filter(
        category=temp_url.category, price__gt=5000
    ).order_by("?")[:4]
    reasons = sorted(
        [r.split("then target prob:") for r in temp_url.rules.split("\n")],
        key=lambda x: float(x[1]),
        reverse=True,
    )
    ctx = {
        "category": temp_url.category,
        "prices": [presents_2000, presents_2001_5000, presents_5000],
        "rules": f"{reasons[0][0]}",
    }
    return render(request, "presents.html", ctx)


def receiver(request):
    url_to_friend = TempUrl.objects.create().questionnaire_uuid
    return redirect("form", form_uuid=url_to_friend)


def giver_self(request):
    request.session["is_giver"] = True
    url_to_friend = TempUrl.objects.create().questionnaire_uuid
    response = redirect("form", form_uuid=url_to_friend)
    return response
