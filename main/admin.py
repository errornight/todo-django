from django.contrib import admin
from . import models
from datetime import datetime
import pytz

class UserAdmin(admin.ModelAdmin):
    list_display = ['name', 'timesince']
    search_fields = ['name']

    @staticmethod
    def timesince(obj):
        now = datetime.now(pytz.utc)
        date = obj.date_joined.replace(tzinfo=pytz.utc)
        elapsed = now - date
        days = elapsed.days
        hours, remainder = divmod(elapsed.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        if days > 0:
            return f"{days} days, {hours} hours ago"
        elif hours > 0:
            return f"{hours} hours, {minutes} minutes ago"
        else:
            return f"{minutes} minutes ago"
        

class TasKAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'status']
    search_fields = ['title', 'description', 'user__username']
    list_filter = ['status']

admin.site.register(models.User,UserAdmin)
admin.site.register(models.Task, TasKAdmin)
