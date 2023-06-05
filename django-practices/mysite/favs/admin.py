from django.contrib import admin
from favs.models import Thing,Fav

# Register your models here.
class ThingAdmin(admin.ModelAdmin):
    exclude = ('picture', 'content_type')

admin.site.register(Thing, ThingAdmin)
admin.site.register(Fav)

