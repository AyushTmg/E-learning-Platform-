from django.contrib import admin
from django.db.models import Count
from django.utils.html import format_html,urlencode
from django.urls import reverse 
from .models import Content,Course,Enrollment

class ContentInline(admin.TabularInline):
    model=Content
    autocomplete_fields=['course']
    extra=20

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display=['id','title','duration','price','is_free','created_at','enrollment_count']
    search_fields = ['title', 'description']
    list_editable=['price']
    inlines=[ContentInline]
    autocomplete_fields=['user']
    list_per_page=10

    @admin.display(ordering='enrollment_count')
    def enrollment_count(self,course):
        url=reverse('admin:elearning_enrollment_changelist')+"?"+urlencode({"course__id":str(course.id)})
        return format_html(f'<a href="{url}" target="_blank">{course.enrollment_count}</a>')
    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(enrollment_count=Count('enrollment'))


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display=['id','course','user','created_at']
    list_per_page=10
    autocomplete_fields=['course','user']
    list_select_related=['user','course']



