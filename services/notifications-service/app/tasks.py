from .models import Notification


def send_emergency_alert(notification_id):
    try:
        notification = Notification.objects.get(id=notification_id)
        notification.is_sent = True
        notification.save()
        return "sent"
    except Notification.DoesNotExist:
        return "Notification not found"


def send_push_notification(notification_id):
    try:
        notification = Notification.objects.get(id=notification_id)
        return "push sent"
    except Notification.DoesNotExist:
        return "Notification not found"
