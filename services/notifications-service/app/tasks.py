from celery import shared_task
from .models import Notification

@shared_task
def send_emergency_alert(notification_id):
    try:
        notification = Notification.objects.get(id=notification_id)
        print(f"Sending emergency alert to: {notification.recipient_email} for {notification.blood_type_needed} at {notification.hospital_name}")
        notification.is_sent = True
        notification.save()
        return "sent"
    except Notification.DoesNotExist:
        print("Notification not found")
        return "Notification not found"

@shared_task
def send_push_notification(notification_id):
    try:
        notification = Notification.objects.get(id=notification_id)
        print(f"Sending push notification to: {notification.recipient_email}")
        return "push sent"
    except Notification.DoesNotExist:
        print("Notification not found")
        return "Notification not found"
