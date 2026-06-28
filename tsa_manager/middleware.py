from django.conf import settings
from django.http import HttpResponse


class ApiCorsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith("/api/") and request.method == "OPTIONS":
            response = HttpResponse(status=204)
            self.add_cors_headers(request, response)
            return response

        response = self.get_response(request)

        if request.path.startswith("/api/"):
            self.add_cors_headers(request, response)

        return response

    def add_cors_headers(self, request, response):
        allowed_origins = settings.CORS_ALLOWED_ORIGINS
        request_origin = request.headers.get("Origin")

        if "*" in allowed_origins:
            response["Access-Control-Allow-Origin"] = "*"
        elif request_origin in allowed_origins:
            response["Access-Control-Allow-Origin"] = request_origin

        response["Vary"] = "Origin"
        response["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
        response["Access-Control-Allow-Headers"] = "Content-Type"
