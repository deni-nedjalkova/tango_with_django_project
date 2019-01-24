from django.shortcuts import render

# first import HttpResponse from django.http module
from django.http import HttpResponse
from rango.models import Category
from rango.models import Page

# a view called index
# each view takes at least one argument - HttpRequest obj
# returns HttpResponse object - takes string as a parameter representing
# the content of the page to be sent to the client
def index(request):
	# return HttpResponse("Rango says hey there partner! <br/><a href='/rango/about/'>About</a>")
	# context_dict = {'boldmessage': "Crunchy, creamy, cookie, candy, cupcake!"}
	context_dict = {}
	category_list = Category.objects.order_by('-likes')[:5]
	# context_dict = {'categories': category_list}
	context_dict['categories'] = category_list
	page_list = Page.objects.order_by('-views')[:5]
	context_dict['pages'] = page_list
	return render(request, 'rango/index.html', context=context_dict)

def about(request):
	#return HttpResponse("Rango says here is the about page. <br/><a href='/rango/'>Index</a>.")
	return render(request, 'rango/about.html')

def show_category(request,category_name_slug):
	# Create a context dictionary which we can pass
	# to the template rendering engine.
	context_dict = {}
	try:
		category = Category.objects.get(slug=category_name_slug)
		pages = Page.objects.filter(category=category)
		context_dict['pages'] = pages
		context_dict['category'] = category
	except Category.DoesNotExist:
		context_dict['category'] = None
		context_dict['pages'] = None

	return render(request, 'rango/category.html', context_dict)
