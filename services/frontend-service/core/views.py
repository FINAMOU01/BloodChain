from django.shortcuts import render
from django.http import JsonResponse


def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def donor_info(request):
    return render(request, 'donor.html')


def login_view(request):
    return render(request, 'login.html')


def register_view(request):
    return render(request, 'register.html')

def register_donor(request):
    return render(request, 'donor/register_donor.html')

def register_hospital(request):
    return render(request, 'hospital/register_hospital.html')


def health(request):
    return JsonResponse({'status': 'ok'})

# Donor pages
def donor_dashboard(request):
    return render(request, 'donor/dashboard.html')

def donor_profile(request):
    return render(request, 'donor/donor_profile.html')

def donor_history(request):
    return render(request, 'donor/donor_history.html')

def donor_appointments(request):
    return render(request, 'donor/donor_appointments.html')

def donor_rewards(request):
    return render(request, 'donor/donor_rewards.html')

def donor_eligibility(request):
    return render(request, 'donor/donor_eligibility.html')

def donor_confirm(request):
    return render(request, 'donor/donor_confirm.html')

def emergency_alerts_donor(request):
    return render(request, 'donor/emergency_alerts.html')

def nearby_hospitals(request):
    return render(request, 'donor/nearby_hospitals.html')

def notification_list_donor(request):
    return render(request, 'donor/notification_list.html')

# Hospital pages
def hospital_dashboard(request):
    return render(request, 'hospital/dashboard.html')

def hospital_profile(request):
    return render(request, 'hospital/hospital_profile.html')

def hospital_confirm(request):
    return render(request, 'hospital/hospital_confirm.html')

def request_form(request):
    return render(request, 'hospital/request_form.html')

def request_list(request):
    return render(request, 'hospital/request_list.html')

def request_detail(request):
    return render(request, 'hospital/request_detail.html')

def stock_detail(request):
    return render(request, 'hospital/stock_detail.html')

def stock_update(request):
    return render(request, 'hospital/stock_update.html')

def donors_nearby(request):
    return render(request, 'hospital/donors_nearby.html')

def notification_list_hospital(request):
    return render(request, 'hospital/notification_list.html')

def create_emergency_alert(request):
    return render(request, 'hospital/create_emergency_alert.html')

# Map pages
def blood_map(request):
    return render(request, 'map/blood_map.html')

# Alerts pages
def emergency_alert(request):
    return render(request, 'alerts/emergency_alert.html')