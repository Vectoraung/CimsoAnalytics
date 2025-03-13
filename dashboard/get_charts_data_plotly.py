
from django.views.decorators.csrf import csrf_exempt
import pandas as pd
from django.http import JsonResponse
import json

@csrf_exempt  # Only use for testing; in production, use CSRF token validation
def age_group_segmentation_plotly(request):
    if request.method == "POST":
        try:
            data = [{
                "x": ["Child", "Adult", "Middle Age", "Elder"],
                "y": [10, 15, 12, 18],
                "type": "bar",
                "marker": { "color": "#419fe3" }
            }]

            titles = {"x_axis_title": "Age Group", "y_axis_title": "Number"}

            print(titles)
            
            return JsonResponse({"data": data, "titles": titles})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    
    return JsonResponse({"error": "Invalid request"}, status=400)

@csrf_exempt  # Only use for testing; in production, use CSRF token validation
def yearly_income_plotly(request):
    if request.method == "POST":
        try:
            data = [{
                "x": ["January", "February", "March", "April"],
                "y": [1000, 1500, 1200, 1800],
                "type": "line",
                "line": { "color": "lineColor", "width": 2 },
                "marker": { "size": 6, "color": "#419fe3" }  
            }]

            titles = {"x_axis_title": "Months", "y_axis_title": "Income"}
            
            return JsonResponse({"data": data, "titles": titles})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    
    return JsonResponse({"error": "Invalid request"}, status=400)

@csrf_exempt  # Only use for testing; in production, use CSRF token validation
def monthly_arrivals_plotly(request):
    if request.method == "POST":
        try:
            data = [{
                "y": ["January", "February", "March", "April", "May", "June",
                    "July", "August", "September", "October", "November", "December"],
                "x": [120, 90, 130, 100, 80, 150, 140, 110, 70, 95, 125, 60], 
                "type": "bar",
                "orientation": "h",
                "marker": { "color": "#419fe3"}
            }]

            titles = {"x_axis_title": "Arrival Bookings", "y_axis_title": "Months"}
            
            return JsonResponse({"data": data, "titles": titles})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    
    return JsonResponse({"error": "Invalid request"}, status=400)