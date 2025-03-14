
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
import random
from datetime import datetime, timedelta
import time

chart_item_colors = [
    "#419fe3",  # Base blue
    "#1e73be",  # Deeper blue
    "#3c7dc1",  # Medium blue
    "#5aa6e8",  # Lighter blue
    "#6cb8f0",  # Sky blue
    "#2b5c8a",  # Dark navy blue
    "#73c2fb",  # Soft blue
    "#1a4d7f",  # Darker blue
    "#85d1ff",  # Light cyan blue
    "#0073e6"   # Vivid blue
]

class ChartLibrary:
    def __init__(self):
        self.chart_data = {}

    def add_chart_data(self, chart_name, filter, data):
        if chart_name not in self.chart_data:
            self.chart_data[chart_name] = []

        self.chart_data[chart_name].append({"filter": filter, "data": data})

chart_library = ChartLibrary()

@csrf_exempt  # Only use for testing; in production, use CSRF token validation
def age_group_segmentation_plotly(request):
    if request.method == "POST":
        try:
            filterValues = json.loads(request.body)

            data = [{
                "x": ["Child", "Adult", "Middle Age", "Elder"],
                "y": [10, 15, 12, 18],
                "type": "bar",
                "marker": { "color": "#419fe3" }
            }]

            titles = {"x_axis_title": "Age Group", "y_axis_title": "Number"}
            
            return JsonResponse({"data": data, "titles": titles})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    
    return JsonResponse({"error": "Invalid request"}, status=400)

@csrf_exempt  # Only use for testing; in production, use CSRF token validation
def yearly_income_plotly(request):
    if request.method == "POST":
        try:
            filterValues = json.loads(request.body)
            print(filterValues)
            data = [{
                "x": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
                "y": [1000, 1500, 1200, 1800, 2000, 2200, 2500, 2800, 3000, 3200, 3500, 3800],
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
            filterValues = json.loads(request.body)
            print(filterValues)
            data = [{
                "y": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
                "x": [120, 90, 130, 100, 80, 150, 140, 110, 70, 95, 125, 60], 
                "type": "bar",
                "orientation": "h",
                "marker": { "color": "#419fe3"}
            }]

            additional_layout_config = {"bargap":0.6}

            titles = {"x_axis_title": "Arrival Bookings", "y_axis_title": "Months"}
            
            return JsonResponse({"data": data, "titles": titles, "additional_layout_config": additional_layout_config})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    
    return JsonResponse({"error": "Invalid request"}, status=400)

@csrf_exempt
def arrivals_plotly(request):
    if request.method == "POST":
        try:
            filterValues = json.loads(request.body)
            print(filterValues)

            data = 54

            chart_library.add_chart_data(filterValues["title"], filterValues["formData"], data)
            
            return JsonResponse({"data": data})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    
    return JsonResponse({"error": "Invalid request"}, status=400)

@csrf_exempt
def cancelled_bookings_plotly(request):
    if request.method == "POST":
        try:
            filterValues = json.loads(request.body)
            print(filterValues)
            data = 54
            
            return JsonResponse({"data": data})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    
    return JsonResponse({"error": "Invalid request"}, status=400)

@csrf_exempt
def departures_bookings_plotly(request):
    if request.method == "POST":
        try:
            filterValues = json.loads(request.body)
            print(filterValues)
            data = 54
            
            return JsonResponse({"data": data})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    
    return JsonResponse({"error": "Invalid request"}, status=400)

@csrf_exempt
def cancelled_bookings_percentage_plotly(request):
    if request.method == "POST":
        try:
            filterValues = json.loads(request.body)
            print(filterValues)
            canceled = 23
            total = 54

            data = [
                {
                    "x": ["Total Bookings"],
                    "y": [canceled],
                    "type": "bar",
                    "name": "Cancelled Bookings",
                    "marker": { "color": chart_item_colors[0] },
                    "hoverinfo": "y",
                    #"showlegend": True,
                },
                {
                    "x": ["Total Bookings"],
                    "y": [total - canceled],
                    "type": "bar",
                    "name": "Successful Bookings",
                    "marker": { "color": chart_item_colors[1] },
                    "hoverinfo": "y",
                    #"showlegend": True,
                }
            ]

            additional_layout_config = {
                "barmode":"stack",
                "legend": {
                    "font": { "size": 12, "color": "#fff" },
                    "bgcolor": "rgba(0, 0, 0, 0)",
                    "bordercolor": "#fff",
                    "borderwidth": 0
                }
                }
            
            return JsonResponse({"data": data, "additional_layout_config": additional_layout_config})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    
    return JsonResponse({"error": "Invalid request"}, status=400)

@csrf_exempt
def frequently_booked_units_plotly(request):
    if request.method == "POST":
        try:
            filterValues = json.loads(request.body)
            print(filterValues)
            unitTypes = ["Deluxe Room", "Suite", "Standard Room", "Penthouse"]
            bookingCounts = [120, 80, 150, 50]
            sliceColors = chart_item_colors[:len(unitTypes)]

            data = [{
                "labels": unitTypes,
                "values": bookingCounts,
                "type": "pie",
                "hole": 0.4,  # Creates the donut effect (0 = full pie, 0.4 = standard donut)
                "marker": { "colors": sliceColors },
                "textinfo": "label+percent",
                "insidetextfont": { "color": "#fff" },
                "showlegend": True
            }]

            additional_layout_config = {
                "legend": {
                    "font": { "size": 12, "color": "#fff" },
                    "bgcolor": "rgba(0, 0, 0, 0)",
                    "bordercolor": "#fff",
                    "borderwidth": 0
                }
                }
            
            return JsonResponse({"data": data, "additional_layout_config": additional_layout_config})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    
    return JsonResponse({"error": "Invalid request"}, status=400)

@csrf_exempt
def member_general_guest_plotly(request):
    if request.method == "POST":
        try:
            filterValues = json.loads(request.body)
            print(filterValues)
            member_guest = 30
            general_guest = 156

            data = [
                {
                    "x": ["Guest Arrivals"],
                    "y": [member_guest],
                    "type": "bar",
                    "name": "member guest arrivals",
                    "marker": { "color": chart_item_colors[0] },
                    "hoverinfo": "y",
                    #"showlegend": True,
                },
                {
                    "x": ["Guest Arrivals"],
                    "y": [general_guest],
                    "type": "bar",
                    "name": "general guest arrivals",
                    "marker": { "color": chart_item_colors[1] },
                    "hoverinfo": "y",
                    #"showlegend": True,
                }
            ]

            additional_layout_config = {
                "barmode":"stack",
                "legend": {
                    "font": { "size": 12, "color": "#fff" },
                    "bgcolor": "rgba(0, 0, 0, 0)",
                    "bordercolor": "#fff",
                    "borderwidth": 0
                }
                }
            
            return JsonResponse({"data": data, "additional_layout_config": additional_layout_config})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    
    return JsonResponse({"error": "Invalid request"}, status=400)

@csrf_exempt
def occupancy_rate_plotly(request):
    if request.method == "POST":
        try:
            filterValues = json.loads(request.body)
            print(filterValues)
            unitTypes = ["Full month", "Occupied"]
            bookingCounts = [100, 30]
            sliceColors = chart_item_colors[:len(unitTypes)]

            data = [{
                "labels": unitTypes,
                "values": bookingCounts,
                "type": "pie",
                "hole": 0,  # Creates the donut effect (0 = full pie, 0.4 = standard donut)
                "marker": { "colors": sliceColors },
                "textinfo": "label+percent",
                "insidetextfont": { "color": "#fff", "size": 6 },
                "showlegend": False
            }]

            additional_layout_config = {
                "legend": {
                    "font": { "size": 12, "color": "#fff" },
                    "bgcolor": "rgba(0, 0, 0, 0)",
                    "bordercolor": "#fff",
                    "borderwidth": 0
                }
                }
            
            return JsonResponse({"data": data, "additional_layout_config": additional_layout_config})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    
    return JsonResponse({"error": "Invalid request"}, status=400)

@csrf_exempt
def average_daily_rate_plotly(request):
    if request.method == "POST":
        try:
            filterValues = json.loads(request.body)
            print(filterValues)
            data = "$82557"
            
            return JsonResponse({"data": data})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    
    return JsonResponse({"error": "Invalid request"}, status=400)

@csrf_exempt
def client_birthdays_plotly(request):
    if request.method == "POST":
        try:
            filterValues = json.loads(request.body)
            print(filterValues)
            first_names = ["Mason", "Emma", "Oliver", "Ava", "Elijah", "Isabella", "William", "Sophia", "James", "Mia"]
            last_names = ["Martin", "Smith", "Johnson", "Williams", "Jones", "Brown", "Davis", "Miller", "Wilson", "Moore"]

            count = 12
            data = []
            for _ in range(count):
                first_name = random.choice(first_names)
                last_name = random.choice(last_names)

                start_date = datetime(1970, 1, 1)
                end_date = datetime(2000, 12, 31)

                time_between_dates = end_date - start_date
                days_between_dates = time_between_dates.days
                random_number_of_days = random.randint(0, days_between_dates)

                birthday = start_date + timedelta(days=random_number_of_days)

                data.append({
                    "firstName": first_name,
                    "lastName": last_name,
                    "birthday": birthday.strftime("%Y-%m-%d")
                })

            return JsonResponse({"data": data})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    
    return JsonResponse({"error": "Invalid request"}, status=400)