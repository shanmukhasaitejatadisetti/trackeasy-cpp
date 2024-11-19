from django.contrib import admin
from .models import Order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'destination', 'goods_type', 'preferred_delivery_date', 'status', 'created_at')
    list_filter = ('status', 'created_at', 'preferred_delivery_date')
    search_fields = ('destination', 'goods_type', 'user__username')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)
