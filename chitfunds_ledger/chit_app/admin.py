from django.contrib import admin
from .models import Profile, ChitFund, Payment, Notification


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'is_approved', 'date_joined')
    list_filter = ('is_approved', 'date_joined')
    search_fields = ('user__username', 'user__email', 'phone_number')
    date_hierarchy = 'date_joined'
    actions = ['approve_users']
    
    def approve_users(self, request, queryset):
        updated = queryset.update(is_approved=True)
        self.message_user(request, f'{updated} users have been approved.')
    approve_users.short_description = "Approve selected users"


@admin.register(ChitFund)
class ChitFundAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'total_amount', 'monthly_amount', 'duration_months', 'start_date', 'end_date')
    list_filter = ('start_date', 'end_date', 'created_at')
    search_fields = ('name', 'user__username', 'description')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('chit_fund', 'amount', 'payment_date', 'payment_method', 'reference_number')
    list_filter = ('payment_date', 'payment_method', 'created_at')
    search_fields = ('chit_fund__name', 'reference_number', 'notes')
    date_hierarchy = 'payment_date'
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('user__username', 'title', 'message')
    date_hierarchy = 'created_at'
    actions = ['mark_as_read']
    
    def mark_as_read(self, request, queryset):
        updated = queryset.update(is_read=True)
        self.message_user(request, f'{updated} notifications have been marked as read.')
    mark_as_read.short_description = "Mark selected notifications as read"
