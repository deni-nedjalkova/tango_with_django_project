from django.shortcuts import render

# first import HttpResponse from django.http module
from django.http import HttpResponse

# a view called index
# each view takes at least one argument - HttpRequest obj
# returns HttpResponse object - takes string as a parameter representing
# the content of the page to be sent to the client
def index(request):
	return HttpResponse("Rango says hey there partner!")
