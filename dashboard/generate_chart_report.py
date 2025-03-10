import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import random
import time
from datetime import datetime, timedelta
from .import report_generator_ai

report_generator = report_generator_ai.ReportGenerator()

@csrf_exempt  # Only use for testing; in production, use CSRF token validation
def generate_report(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            request_context = {
                "Chart title": data["chart_title"],
                #"filters": data["filters"] if "filters" in data else None,
                "data": data["data"][-1]
            }

            report = report_generator.generate_report(request_context)
            return JsonResponse({"report": report})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    
    return JsonResponse({"error": "Invalid request"}, status=400)