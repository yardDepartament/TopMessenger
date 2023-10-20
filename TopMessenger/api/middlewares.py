from django.http import HttpResponseForbidden

from django.http import JsonResponse

class CheckRefererMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        referer = request.META.get('HTTP_REFERER')
        if referer is not None and 'localhost:3000' not in referer:
            return JsonResponse({'error': 'Доступ запрещен'}, status=403)
        return self.get_response(request)
