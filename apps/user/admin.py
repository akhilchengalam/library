from django.contrib import admin
from .models import Profile

# Register your models here.
class BookAdmin(admin.ModelAdmin):
    fields = all
    class meta:
        model = Profile

admin.site.register(Profile)