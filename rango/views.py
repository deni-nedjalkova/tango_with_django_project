from django.shortcuts import render

# first import HttpResponse from django.http module
from django.http import HttpResponse

# a view called index
# each view takes at least one argument - HttpRequest obj
# returns HttpResponse object - takes string as a parameter representing
# the content of the page to be sent to the client
def index(request):
	return HttpResponse("Rango says hey there partner! <br/><a href='/rango/about/'>About</a>")
	#context_dict = {'boldmessage': "Crunchy, creamy, cookie, candy, cupcake!"}
	#return render(request, 'rango/index.html', context=context_dict)

def about(request):
	return HttpResponse("Rango says here is the about page. <br/><a href='/rango/''>Index</a>.")
