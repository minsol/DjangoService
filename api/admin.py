from django.contrib import admin
from .models import Student #记得导包

# Register your models here.
 
@admin.register(Student)
class BlogTypeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name') 