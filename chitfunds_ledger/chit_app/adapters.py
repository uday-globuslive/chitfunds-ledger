from allauth.account.adapter import DefaultAccountAdapter
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse
from django.contrib.sites.models import Site


class CustomAccountAdapter(DefaultAccountAdapter):
    """Custom adapter for django-allauth to handle user registration and approval"""
    
    def is_open_for_signup(self, request):
        """Whether to allow sign ups"""
        return getattr(settings, 'ACCOUNT_ALLOW_SIGNUPS', True)
    
    def get_login_redirect_url(self, request):
        """Redirect to dashboard after login"""
        return reverse('dashboard')
    
    def confirm_email(self, request, email_address):
        """Custom email confirmation to also approve user"""
        # Call the parent confirm_email method
        super().confirm_email(request, email_address)
        
        # Also approve the user automatically
        user = email_address.user
        profile = user.profile
        profile.is_approved = True
        profile.save()
        
        # Create welcome notification
        from .models import Notification
        Notification.objects.create(
            user=user,
            title='Welcome to ChitFunds Ledger',
            message='Your email has been verified and account approved. You can now add your chit funds and track payments.'
        )
        
        return user


def send_approval_email(user):
    """Send an email to the user when their account is approved by an admin"""
    current_site = Site.objects.get_current()
    subject = 'Your ChitFunds Ledger Account has been Approved'
    message = render_to_string('chit_app/email/approval_email.html', {
        'user': user,
        'domain': current_site.domain,
        'protocol': 'https' if settings.SECURE_SSL_REDIRECT else 'http',
    })
    
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
        html_message=message
    )
    
    return True
