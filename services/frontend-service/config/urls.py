from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from core import views

urlpatterns = [
    path('health/', views.health),
    path('login/', views.login_view),
    path('register/', views.register_view),
    path('', views.index),
    path('register/donor/', views.register_donor),
    path('register/hospital/', views.register_hospital),
      # Donor URLs
    path('donor/dashboard/', views.donor_dashboard),
    path('donor/profile/', views.donor_profile),
    path('donor/history/', views.donor_history),
    path('donor/appointments/', views.donor_appointments),
    path('donor/rewards/', views.donor_rewards),
    path('donor/eligibility/', views.donor_eligibility),
    path('donor/confirm/', views.donor_confirm),
    path('donor/alerts/', views.emergency_alerts_donor),
    path('donor/hospitals/', views.nearby_hospitals),
    path('donor/notifications/', views.notification_list_donor),

    # Hospital URLs
    path('hospital/dashboard/', views.hospital_dashboard),
    path('hospital/profile/', views.hospital_profile),
    path('hospital/confirm/', views.hospital_confirm),
    path('hospital/request/new/', views.request_form),
    path('hospital/requests/', views.request_list),
    path('hospital/request/detail/', views.request_detail),
    path('hospital/stock/', views.stock_detail),
    path('hospital/stock/update/', views.stock_update),
    path('hospital/donors/', views.donors_nearby),
    path('hospital/notifications/', views.notification_list_hospital),
    path('hospital/alerts/create/', views.create_emergency_alert),
    path('map/', views.blood_map),
    path('alerts/emergency/', views.emergency_alert),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
