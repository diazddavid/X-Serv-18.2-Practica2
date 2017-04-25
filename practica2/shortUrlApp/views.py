from django.shortcuts import render

from django.template.loader import get_template
from django.template import Context
from shortUrlApp.models import Page
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect

# Create your views here.

def form():
    toReturn = "<html><body><h1>Introduzca URL a acortar: </h1>"
    toReturn += "<form action='/'' method='post'>"
    toReturn += "URL:<br> <input type='text' name = 'url' value='google.es'><br>"
    toReturn += "<input type='submit' value='Submit'>"
    toReturn += "</form></body>"
    toReturn += "</br>Tengo guardadas:"
    return(toReturn)

@csrf_exempt
def default(request):
    if request.method == "GET":
        toReturn = form()
        for page in Page.objects.all():
            toReturn += "</br> <a href=/" + str(page.id) + ">" + str(page.id) + "</a> "
            toReturn += " ==> <a href=/" + page.url + ">" + page.url + "</a>"
        toReturn +=  "</html>"
        return HttpResponse(toReturn)

    if request.method == "POST" or request.method == "PUT":
        toParse = request.body.decode('utf-8')
        newUrl = toParse.split('=')[1]
        if not newUrl.startswith("http://"):
            newUrl = "http://" + newUrl
        try:
            page = Page.objects.get(url = newUrl)
            toReturn += "Su pagina ya estaba acortada, su pagina:"
        except ObjectDoesNotExist:
            page = Page(url = newUrl)
            page.save()
            toReturn += "Su pagina:"
        toReturn += "<a href=/" + page.url + ">" + page.url + "</a>"
        toReturn += "</br>Acortada es: <a href=/" + str(page.id) + ">" + str(page.id) + "</a> "
        return HttpResponse(toReturn)

def redirect(request, toRedirect):
    try:
        page = Page.objects.get(id = toRedirect)
        return HttpResponse("<meta http-equiv='refresh' content='0; url=" + page.url + "'/>", status = 303)
    except ObjectDoesNotExist:
        toReturn = "La url acortada proporcionada no existe,pulse"
        toReturn += "<a href=/> aqui </a> para acortarla:"
        return HttpResponse(toReturn)
