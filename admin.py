from django.contrib import admin
from .models import Orders, OrderItems, Feedbacks, Users, Products, PickupPoints, DeliveryPoints

class OrderItemsInline(admin.TabularInline):
    model = OrderItems
    extra = 0
    

@admin.register(Orders)
class OrdersAdmin(admin.ModelAdmin):

    list_display = ('order_number', 'user_id', 'total_amount', 'status', 'delivery_date')

    list_editable = ('status',)

    list_filter = ('status', 'delivery_date')

    search_fields = ('order_number',)

    inlines = [OrderItemsInline]

@admin.register(Feedbacks)
class FeedbacksAdmin(admin.ModelAdmin):

    list_display = ('user', 'product', 'rating', 'comment', 'order')

    list_filter = ('rating',)

    search_fields = ('user__full_name', 'comment')

admin.site.register(Users)
admin.site.register(Products)
admin.site.register(PickupPoints)
admin.site.register(DeliveryPoints)

admin.site.site_header = "Панель администрирования"
admin.site.site_title = "Панель администрирования"
admin.site.index_title = "Добро пожаловать в панель управления FoodStore"



