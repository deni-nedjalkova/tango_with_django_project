from django.shortcuts import render

# first import HttpResponse from django.http module
from django.http import HttpResponse
from rango.models import Category
from rango.models import Page
from rango.forms import CategoryForm, PageForm
from rango.forms import UserForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from datetime import datetime

# a view called index
# each view takes at least one argument - HttpRequest obj
# returns HttpResponse object - takes string as a parameter representing
# the content of the page to be sent to the client

# A helper method
def get_server_side_cookie(request, cookie, default_val=None):
	val = request.session.get(cookie)
	if not val:
		val = default_val
	return val

def visitor_cookie_handler(request):
	# Get the number of visits to the site.
	# We use the COOKIES.get() function to obtain the visits cookie.
	# If the cookie exists, the value returned is casted to an integer.
	# If the cookie doesn't exist, then the default value of 1 is used.
	visits = int(get_server_side_cookie(request, 'visits', '1'))
	last_visit_cookie = get_server_side_cookie(request,
												'last_visit',
												str(datetime.now()))
	last_visit_time = datetime.strptime(last_visit_cookie[:-7],
												'%Y-%m-%d %H:%M:%S')
	# If it's been more than a day since the last visit...
	if (datetime.now() - last_visit_time).days > 0:
		visits = visits + 1
		#update the last visit cookie now that we have updated the count
		request.session['last_visit'] = str(datetime.now())
	else:
		# set the last visit cookie
		request.session['last_visit'] = last_visit_cookie
	
	# Update/set the visits cookie
	request.session['visits'] = visits

def index(request):
	request.session.set_test_cookie()
	# return HttpResponse("Rango says hey there partner! <br/><a href='/rango/about/'>About</a>")
	# context_dict = {'boldmessage': "Crunchy, creamy, cookie, candy, cupcake!"}
	context_dict = {}
	category_list = Category.objects.order_by('-likes')[:5]
	# context_dict = {'categories': category_list}
	context_dict['categories'] = category_list
	page_list = Page.objects.order_by('-views')[:5]
	context_dict['pages'] = page_list

	visitor_cookie_handler(request)
	context_dict['visits'] = request.session['visits']

	response = render(request, 'rango/index.html', context=context_dict)

	return response

def about(request):
	if request.session.test_cookie_worked():
		print("TEST COOKIE WORKED!")
		request.session.delete_test_cookie()

	context_dict = {}

	visitor_cookie_handler(request)
	context_dict['visits'] = request.session['visits']

	#return HttpResponse("Rango says here is the about page. <br/><a href='/rango/'>Index</a>.")
	
	response = render(request, 'rango/about.html', context=context_dict)

	return response

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

def add_category(request):
	form = CategoryForm()

	# A HTTP POST?
	if request.method == 'POST':
		form = CategoryForm(request.POST)

		# Have we been provided with a valid form?
		if form.is_valid():
			# Save the new category to the database.
			form.save(commit=True)
			print(category, category.slug)
			# Recently category added is on the index page --
			# Direct the user back to the index page
			return index(request)
		else:
			print(form.errors)

	return render(request, 'rango/add_category.html', {'form': form})

def add_page(request, category_name_slug):
	try:
		category = Category.objects.get(slug=category_name_slug)
	except Category.DoesNotExist:
		category = None

	form = PageForm()
	if request.method == 'POST':
		form = PageForm(request.POST)
		
		if form.is_valid():
			if category:
				page = form.save(commit=False)
				page.category = category
				page.views = 0
				page.save()
				return show_category(request, category_name_slug)
		else:
			print(form.errors)

	context_dict = {'form':form, 'category': category}
	return render(request, 'rango/add_page.html', context_dict)

def register(request):
	# A boolean value for telling the template
	# whether the registration was successful.
	registered = False
	
	# POST: processing form data.
	if request.method == 'POST':
		# Attempt to grab information from the raw form information.
		user_form = UserForm(data=request.POST)
		profile_form = UserProfileForm(data=request.POST)
		
		# If the two forms are valid...
		if user_form.is_valid() and profile_form.is_valid():
			# Save the user's form data to the database.
			user = user_form.save()
			# Now we hash the password with the set_password method
			user.set_password(user.password)
			user.save()
			
			# Since we need to set the user attribute ourselves,
			# we set commit=False. This delays saving the model
			# until we're ready to avoid integrity problems.
			profile = profile_form.save(commit=False)

			# reference of the User instance in the UserProfile
			# populate the user attribute of the UserProfileForm form
			profile.user = user
			
			if 'picture' in request.FILES:
				profile.picture = request.FILES['picture']
			
			profile.save()
			
			# registration was successful.
			registered = True
		
		else:
			print(user_form.errors, profile_form.errors)
			
	else:
		# Not a HTTP POST, so we render our form using two ModelForm instances.
		# These forms will be blank, ready for user input.
		user_form = UserForm()
		profile_form = UserProfileForm()
		
	# Render the template depending on the context.
	return render(request, 'rango/register.html',
	{'user_form': user_form, 'profile_form': profile_form, 'registered': registered})

def user_login(request):
	# HTTP POST: try to pull out the relevant information.
	if request.method == 'POST':
		# This information is obtained from the login form.
		# request.POST.get('<variable>') returns None if the
		# value does not exist
		username = request.POST.get('username')
		password = request.POST.get('password')
		
		# check if combination is valid - a User object is returned if it is.
		user = authenticate(username=username, password=password)
		
		# If we have a User object, the details are correct.
		if user:
			# Is the account active? It could have been disabled.
			if user.is_active:
				login(request, user)
				return HttpResponseRedirect(reverse('index'))
			else:
				# An inactive account was used - no logging in!
				return HttpResponse("Your Rango account is disabled.")
		
		else:
			# Bad login details were provided.
			print("Invalid login details: {0}, {1}".format(username, password))
			return HttpResponse("Invalid login details supplied.")
		
		# The request is not a HTTP POST, so display the login form.
		# This scenario would most likely be a HTTP GET.
	else:
		return render(request, 'rango/login.html', {})

@login_required
def restricted(request):
	print ("Since you're logged in, you can see this text!")
	return render(request, 'rango/restricted.html')

# Use the login_required decorator to ensure only those logged in can
# access the view
@login_required
def user_logout(request):
	# Since we know the user is logged in, we can now just log them out
	logout(request)
	# transition back to the homepage
	return HttpResponseRedirect(reverse('index'))