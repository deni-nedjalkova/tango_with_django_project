from django.db import models

# Create your models here.

class Category(models.Model):
	name = models.CharField(max_length=128, unique=True)

	def __str__(self):
	# generate string representation of the class
		return self.name


class Page(models.Model):
	# Category is specified as an argument to the field's constructor
	category = models.ForeignKey(Category)
	title = models.CharField(max_length=128)
	url = models.URLField()
	views = models.IntegerField(default=0)

	def __str__(self):
		return self.title
