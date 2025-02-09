from django.contrib import admin

from .models import *


admin.site.register(CustomUser)
admin.site.register(TimezoneDict)
admin.site.register(PropertyCode)
admin.site.register(UserProperty)
admin.site.register(StatusDict)
admin.site.register(UserSending)
admin.site.register(Report)
admin.site.register(UserReportLink)
