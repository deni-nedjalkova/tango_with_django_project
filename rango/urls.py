from django.conf.urls import url
from rango import views

urlpatterns = [
	# allows to call the function url and point to the index view
	# for the mapping in urlpatterns
	url(r'^$', views.index, name='index'),
	url(r'^about/', views.about, name='about'),
]