from django.http import HttpResponse
from django.views import View
from .tasks import send_notification_to_subscribers

class IndexView(View):
    def get(self, request):
        send_notification_to_subscribers.delay()
        return HttpResponse('Hello!')