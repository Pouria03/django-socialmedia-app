from django.contrib import admin
from . import models
# Register your models here.


class PostAdmin(admin.ModelAdmin):
    list_display = ('user','slug','created_date','updated_date')
    search_fields = ('slug','body')
    prepopulated_fields = {'slug':('body',)}
    raw_id_fields =('user',)

admin.site.register(models.Post,PostAdmin)

admin.site.register(models.Comment)
admin.site.register(models.PostLike)