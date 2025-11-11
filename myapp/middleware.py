# middleware.py
import threading

thread_local = threading.local()


class AuditoriaMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        thread_local.user = getattr(request, 'user', None)
        response = self.get_response(request)
        return response

