from django.contrib import admin
from .models import Question, Choice

# Register your models here.


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['question_text']}),
        ('Date information', {'fields': ['publish_date'],
                              'classes':['collapse']})
    ]
    inlines = [ChoiceInline]

    # admin list page configuration i.e. which column to display
    list_display = ('question_text', 'publish_date', 'was_published_recently')
    # admin page list view page filter optoin (right side widget)
    list_filter = ['publish_date']
    # to display search box top of change list
    search_fields = ['question_text']


admin.site.register(Question, QuestionAdmin)
