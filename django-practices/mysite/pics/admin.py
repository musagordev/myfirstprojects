from django.contrib import admin
from pics.models import Pic

# Register your models here.
class PicAdmin(admin.ModelAdmin):
    exclude = ('picture', 'content_type')

admin.site.register(Pic, PicAdmin)