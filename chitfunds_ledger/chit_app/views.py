from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.db.models import Sum
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator

from .models import ChitFund, Payment, Profile, Notification, User
from .forms import (
    UserRegisterForm, UserUpdateForm, ProfileUpdateForm, 
    ChitFundForm, PaymentForm, PaymentFilterForm
)
from .adapters import send_approval_email


# Home, Dashboard and Profile Views
def home(request):
    """Landing page for the application"""
    return render(request, 'chit_app/home.html')


@login_required
def dashboard(request):
    """User dashboard showing summary of all chit funds"""
    chit_funds = ChitFund.objects.filter(user=request.user).order_by('-created_at')
    recent_payments = Payment.objects.filter(chit_fund__user=request.user).order_by('-payment_date')[:5]
    notifications = Notification.objects.filter(user=request.user, is_read=False)[:5]
    
    total_invested = ChitFund.objects.filter(user=request.user).aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    total_paid = sum(chit_fund.total_paid() for chit_fund in chit_funds)
    remaining_amount = total_invested - total_paid
    
    context = {
        'chit_funds': chit_funds,
        'recent_payments': recent_payments,
        'notifications': notifications,
        'total_invested': total_invested,
        'total_paid': total_paid,
        'remaining_amount': remaining_amount,
    }
    return render(request, 'chit_app/dashboard.html', context)


@login_required
def profile(request):
    """User profile view and update form"""
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, instance=request.user.profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
        
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'chit_app/profile.html', context)


# Registration and Account Views
def register(request):
    """User registration view"""
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create user profile
            Profile.objects.create(user=user)
            messages.success(request, 'Your account has been created! Please wait for admin approval or verify your email.')
            return redirect('account_login')
    else:
        form = UserRegisterForm()
    return render(request, 'chit_app/register.html', {'form': form})


@method_decorator(staff_member_required, name='dispatch')
class UserApprovalListView(ListView):
    """Admin view to show users waiting for approval"""
    model = Profile
    template_name = 'chit_app/user_approval_list.html'
    context_object_name = 'profiles'
    
    def get_queryset(self):
        return Profile.objects.filter(is_approved=False)


@staff_member_required
def approve_user(request, pk):
    """Admin view to approve a user"""
    profile = get_object_or_404(Profile, pk=pk)
    profile.is_approved = True
    profile.save()
    
    # Send approval email to user
    send_approval_email(profile.user)
    
    # Create notification for the user
    Notification.objects.create(
        user=profile.user,
        title='Account Approved',
        message='Your account has been approved. You can now add chit funds and track your payments.'
    )
    
    messages.success(request, f'The user {profile.user.username} has been approved!')
    return redirect('user_approval_list')


# ChitFund Views
class ChitFundListView(LoginRequiredMixin, ListView):
    """List all chit funds for the logged-in user"""
    model = ChitFund
    template_name = 'chit_app/chitfund_list.html'
    context_object_name = 'chit_funds'
    ordering = ['-created_at']
    
    def get_queryset(self):
        return ChitFund.objects.filter(user=self.request.user)


class ChitFundDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    """Detailed view of a specific chit fund"""
    model = ChitFund
    template_name = 'chit_app/chitfund_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        chit_fund = self.get_object()
        context['payments'] = Payment.objects.filter(chit_fund=chit_fund).order_by('-payment_date')
        context['payment_form'] = PaymentForm()
        context['filter_form'] = PaymentFilterForm()
        return context
    
    def test_func(self):
        chit_fund = self.get_object()
        return self.request.user == chit_fund.user


class ChitFundCreateView(LoginRequiredMixin, CreateView):
    """Create a new chit fund"""
    model = ChitFund
    form_class = ChitFundForm
    template_name = 'chit_app/chitfund_form.html'
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ChitFundUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Update an existing chit fund"""
    model = ChitFund
    form_class = ChitFundForm
    template_name = 'chit_app/chitfund_form.html'
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        chit_fund = self.get_object()
        return self.request.user == chit_fund.user


class ChitFundDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Delete a chit fund"""
    model = ChitFund
    template_name = 'chit_app/chitfund_confirm_delete.html'
    success_url = reverse_lazy('chitfund_list')
    
    def test_func(self):
        chit_fund = self.get_object()
        return self.request.user == chit_fund.user


# Payment Views
class PaymentCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """Create a new payment for a chit fund"""
    model = Payment
    form_class = PaymentForm
    template_name = 'chit_app/payment_form.html'
    
    def setup(self, request, *args, **kwargs):
        self.chit_fund_id = kwargs.get('chit_fund_id')
        return super().setup(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['chit_fund'] = get_object_or_404(ChitFund, id=self.chit_fund_id, user=self.request.user)
        return context
    
    def form_valid(self, form):
        form.instance.chit_fund = get_object_or_404(ChitFund, id=self.chit_fund_id, user=self.request.user)
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('chit_fund_detail', kwargs={'pk': self.chit_fund_id})
    
    def test_func(self):
        chit_fund = get_object_or_404(ChitFund, id=self.chit_fund_id)
        return self.request.user == chit_fund.user


@login_required
def add_payment(request, pk):
    """AJAX view to add a payment directly from the chit fund detail page"""
    chit_fund = get_object_or_404(ChitFund, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = PaymentForm(request.POST, request.FILES)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.chit_fund = chit_fund
            payment.save()
            messages.success(request, 'Payment added successfully!')
            return redirect('chit_fund_detail', pk=chit_fund.pk)
    else:
        form = PaymentForm()
    
    context = {
        'form': form,
        'chit_fund': chit_fund,
    }
    return render(request, 'chit_app/payment_form.html', context)


class PaymentDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    """Detailed view of a specific payment"""
    model = Payment
    template_name = 'chit_app/payment_detail.html'
    
    def test_func(self):
        payment = self.get_object()
        return self.request.user == payment.chit_fund.user


class PaymentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Update an existing payment"""
    model = Payment
    form_class = PaymentForm
    template_name = 'chit_app/payment_form.html'
    
    def get_success_url(self):
        return reverse('chit_fund_detail', kwargs={'pk': self.object.chit_fund.pk})
    
    def test_func(self):
        payment = self.get_object()
        return self.request.user == payment.chit_fund.user


class PaymentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Delete a payment"""
    model = Payment
    template_name = 'chit_app/payment_confirm_delete.html'
    
    def get_success_url(self):
        return reverse('chit_fund_detail', kwargs={'pk': self.object.chit_fund.pk})
    
    def test_func(self):
        payment = self.get_object()
        return self.request.user == payment.chit_fund.user


# Notification Views
@login_required
def notification_list(request):
    """List all notifications for the logged-in user"""
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'chit_app/notification_list.html', {'notifications': notifications})


@login_required
def mark_notification_read(request, pk):
    """Mark a notification as read"""
    notification = get_object_or_404(Notification, pk=pk, user=request.user)
    notification.is_read = True
    notification.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('notification_list')))


@login_required
def mark_all_notifications_read(request):
    """Mark all notifications as read"""
    Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
    messages.success(request, 'All notifications marked as read!')
    return redirect('notification_list')
