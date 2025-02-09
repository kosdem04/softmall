from django.contrib import admin

from .models import *


admin.site.register(UserGroup)
admin.site.register(RolesDict)
admin.site.register(UserRoles)
admin.site.register(FunctionsDict)
admin.site.register(RoleFunctions)

