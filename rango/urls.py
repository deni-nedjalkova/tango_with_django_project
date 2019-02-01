from django.conf.urls import url
from rango import views

urlpatterns = [
	# allows to call the function url and point to the index view
	# for the mapping in urlpatterns
	url(r'^$', views.index, name='index'),
	url(r'^about/', views.about, name='about'),
	url(r'^add_category/$', views.add_category, name='add_category'),
	url(r'^category/(?P<category_name_slug>[\w\-]+)/$', views.show_category, name='show_category'),
]