from django.contrib import admin
from . import models

# Register your models here  :
class RelationAdmin(admin.ModelAdmin):
    list_display = ('from_user','to_user','start_following_date')
    search_fields = ('from_user',)

admin.site.register(models.Relation,RelationAdmin)