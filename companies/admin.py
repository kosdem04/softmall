from django.contrib import admin

from .models import *


admin.site.register(Company)
admin.site.register(License)
admin.site.register(Module)
admin.site.register(ModuleCompanyLink)
admin.site.register(CompanyProperty)
admin.site.register(Department)

