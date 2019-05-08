from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from main.models import Specialist, Service, Order, Seance, Category
# from main.models import User

admin.site.register(Seance)
admin.site.register(Order)
admin.site.register(Service)
admin.site.register(Specialist)
admin.site.register(Category)
# admin.site.unregister(User)
admin.site.unregister(Group)

# admin.site.register(User, UserAdmin)
