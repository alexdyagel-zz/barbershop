from django.contrib import admin
from django.contrib.auth.models import Group

from main.models import Specialist, Service, Order, Seance, Category


class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price')
    list_display_links = ('name',)
    search_fields = ('category__name', 'name', 'price')


class SeanceAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'time', 'specialist', 'reserved')
    list_display_links = ('id',)
    search_fields = ('date', 'time', 'specialist__name')


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'service', 'seance', 'user')
    list_display_links = ('id',)
    search_fields = ('user__username',)


admin.site.register(Order, OrderAdmin)
admin.site.register(Seance, SeanceAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Specialist)
admin.site.register(Category)
admin.site.unregister(Group)
