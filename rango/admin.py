from django.contrib import admin
from rango.models import Category, Page, UserProfile
from rango.models import Question, Choice

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug':('name', )}

admin.site.register(Category, CategoryAdmin)

class ChoiceInline(admin.TabularInline):
    model = Choice
    # numberof slots
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
	fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
	inlines = [ChoiceInline]
	list_display = ('question_text', 'pub_date', 'was_published_recently')
	list_filter = ['pub_date']
	search_fields = ['question_text']

admin.site.register(Question, QuestionAdmin)

class PageAdmin(admin.ModelAdmin):
	list_display = ('title', 'category', 'url')

admin.site.register(Page, PageAdmin)

admin.site.register(UserProfile)