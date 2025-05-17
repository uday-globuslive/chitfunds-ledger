from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
import uuid
import os


def receipt_upload_path(instance, filename):
    """Generate file path for receipt images"""
    # Get the file extension
    ext = filename.split('.')[-1]
    # Generate a unique filename using UUID
    new_filename = f"{uuid.uuid4()}.{ext}"
    # Return the file path
    return os.path.join('receipts', instance.chit_fund.name, new_filename)


class Profile(models.Model):
    """User profile with additional fields"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    is_approved = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"


class ChitFund(models.Model):
    """Represents a Chit Fund scheme"""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    duration_months = models.PositiveIntegerField()
    monthly_amount = models.DecimalField(max_digits=12, decimal_places=2)
    organizer = models.CharField(max_length=100, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chit_funds')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('chit_fund_detail', kwargs={'pk': self.pk})
    
    def total_paid(self):
        """Calculate total amount paid so far"""
        return sum(payment.amount for payment in self.payments.all())
    
    def remaining_amount(self):
        """Calculate remaining amount to be paid"""
        return self.total_amount - self.total_paid()
    
    def payment_progress(self):
        """Calculate payment progress as percentage"""
        if self.total_amount == 0:
            return 0
        return (self.total_paid() / self.total_amount) * 100
    
    def next_payment_date(self):
        """Calculate the next payment date"""
        last_payment = self.payments.order_by('-payment_date').first()
        if not last_payment:
            return self.start_date
        
        # Calculate next month from the last payment date
        next_date = last_payment.payment_date
        next_date = next_date.replace(month=next_date.month + 1) if next_date.month < 12 else next_date.replace(year=next_date.year + 1, month=1)
        return next_date


class Payment(models.Model):
    """Represents a payment made towards a Chit Fund"""
    chit_fund = models.ForeignKey(ChitFund, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_date = models.DateField(default=timezone.now)
    payment_method = models.CharField(max_length=50)
    reference_number = models.CharField(max_length=100, blank=True)
    receipt_image = models.ImageField(upload_to=receipt_upload_path, blank=True, null=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Payment of {self.amount} for {self.chit_fund.name} on {self.payment_date}"
    
    def get_absolute_url(self):
        return reverse('payment_detail', kwargs={'pk': self.pk})


class Notification(models.Model):
    """Notification system for updates and reminders"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=100)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-created_at']
