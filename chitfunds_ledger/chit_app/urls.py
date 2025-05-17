from django.urls import path
from . import views

urlpatterns = [
    # Home and Dashboard
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # User Profile
    path('profile/', views.profile, name='profile'),
    
    # Registration and User Approval
    path('register/', views.register, name='register'),
    path('admin/user-approval/', views.UserApprovalListView.as_view(), name='user_approval_list'),
    path('admin/approve-user/<int:pk>/', views.approve_user, name='approve_user'),
    
    # ChitFund URLs
    path('chitfunds/', views.ChitFundListView.as_view(), name='chitfund_list'),
    path('chitfunds/new/', views.ChitFundCreateView.as_view(), name='chitfund_create'),
    path('chitfunds/<int:pk>/', views.ChitFundDetailView.as_view(), name='chit_fund_detail'),
    path('chitfunds/<int:pk>/update/', views.ChitFundUpdateView.as_view(), name='chitfund_update'),
    path('chitfunds/<int:pk>/delete/', views.ChitFundDeleteView.as_view(), name='chitfund_delete'),
    
    # Payment URLs
    path('chitfunds/<int:chit_fund_id>/payment/new/', views.PaymentCreateView.as_view(), name='payment_create'),
    path('chitfunds/<int:pk>/add-payment/', views.add_payment, name='add_payment'),
    path('payments/<int:pk>/', views.PaymentDetailView.as_view(), name='payment_detail'),
    path('payments/<int:pk>/update/', views.PaymentUpdateView.as_view(), name='payment_update'),
    path('payments/<int:pk>/delete/', views.PaymentDeleteView.as_view(), name='payment_delete'),
    
    # Notification URLs
    path('notifications/', views.notification_list, name='notification_list'),
    path('notifications/<int:pk>/mark-read/', views.mark_notification_read, name='mark_notification_read'),
    path('notifications/mark-all-read/', views.mark_all_notifications_read, name='mark_all_notifications_read'),
]
