import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import random
import time
from datetime import datetime, timedelta

@csrf_exempt  # Only use for testing; in production, use CSRF token validation
def get_arrivals_count(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            data_value = random.randint(10, 50)
            time.sleep(random.randint(2, 4))
            return JsonResponse({"data_value": data_value})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    
    return JsonResponse({"error": "Invalid request"}, status=400)

@csrf_exempt  # Only use for testing; in production, use CSRF token validation
def get_departures_count(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            data_value = random.randint(10, 50)
            time.sleep(random.randint(2, 4))
            return JsonResponse({"data_value": data_value})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    
    return JsonResponse({"error": "Invalid request"}, status=400)

@csrf_exempt  # Only use for testing; in production, use CSRF token validation
def get_cancelled_bookings_count(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            data_value = random.randint(10, 50)
            time.sleep(random.randint(2, 4))
            return JsonResponse({"data_value": data_value})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    
    return JsonResponse({"error": "Invalid request"}, status=400)

@csrf_exempt  # Only use for testing; in production, use CSRF token validation
def get_cancelled_bookings_percentage(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            data_value = f'{random.randint(10, 50)}%'
            time.sleep(random.randint(2, 4))
            return JsonResponse({"data_value": data_value})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    
    return JsonResponse({"error": "Invalid request"}, status=400)

@csrf_exempt  # Only use for testing; in production, use CSRF token validation
def booking_arrivals_yearly(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            months = [
                "Jan", "Feb", "Mar", "Apr", "May", "Jun",
                "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
            ]

            bookings = [random.randint(50, 550) for _ in months]

            data_value = {"months": months, "bookings": bookings}
            time.sleep(random.randint(2, 4))
            return JsonResponse({"data_value": data_value})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    
    return JsonResponse({"error": "Invalid request"}, status=400)

@csrf_exempt  # Only use for testing; in production, use CSRF token validation
def client_birthdays(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            first_names = ["Mason", "Emma", "Oliver", "Ava", "Elijah", "Isabella", "William", "Sophia", "James", "Mia"]
            last_names = ["Martin", "Smith", "Johnson", "Williams", "Jones", "Brown", "Davis", "Miller", "Wilson", "Moore"]

            count = 12
            people = []
            for _ in range(count):
                first_name = random.choice(first_names)
                last_name = random.choice(last_names)

                start_date = datetime(1970, 1, 1)
                end_date = datetime(2000, 12, 31)

                time_between_dates = end_date - start_date
                days_between_dates = time_between_dates.days
                random_number_of_days = random.randint(0, days_between_dates)

                birthday = start_date + timedelta(days=random_number_of_days)

                people.append({
                    "firstName": first_name,
                    "lastName": last_name,
                    "birthday": birthday.strftime("%Y-%m-%d")
                })

            time.sleep(random.randint(2, 4))

            return JsonResponse({"data_value": people})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    
    return JsonResponse({"error": "Invalid request"}, status=400)

@csrf_exempt  # Only use for testing; in production, use CSRF token validation
def member_guest_arrivals_count(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            data_value = random.randint(10, 50)
            time.sleep(random.randint(2, 4))
            return JsonResponse({"data_value": data_value})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    
    return JsonResponse({"error": "Invalid request"}, status=400)

@csrf_exempt  # Only use for testing; in production, use CSRF token validation
def general_guest_arrivals_count(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            data_value = random.randint(10, 50)
            time.sleep(random.randint(2, 4))
            return JsonResponse({"data_value": data_value})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    
    return JsonResponse({"error": "Invalid request"}, status=400)

@csrf_exempt  # Only use for testing; in production, use CSRF token validation
def most_frequently_units(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            data_value = [
                { "ranking": 1, "unit": "Premium", "bookings": 152 },
                { "ranking": 2, "unit": "Silver", "bookings": 51 },
                { "ranking": 3, "unit": "Platinum", "bookings": 23 },
                { "ranking": 4, "unit": "Gold", "bookings": 18 },
                { "ranking": 5, "unit": "Economy", "bookings": 12 }
            ]
            time.sleep(random.randint(2, 4))
            return JsonResponse({"data_value": data_value})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    
    return JsonResponse({"error": "Invalid request"}, status=400)

@csrf_exempt  # Only use for testing; in production, use CSRF token validation
def age_group_segmentation(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            age_group = ["Child", "Adult", "Middle Age", "Elder"]
            data_value = []
            for age in age_group:
                data_value.append({"age_group":age, "count": random.randint(10, 50)})
            time.sleep(random.randint(2, 4))
            return JsonResponse({"data_value": data_value})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    
    return JsonResponse({"error": "Invalid request"}, status=400)

@csrf_exempt  # Only use for testing; in production, use CSRF token validation
def occupancy_rate(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            data_value = f"{random.randint(10, 50)}%"
            time.sleep(random.randint(2, 4))
            return JsonResponse({"data_value": data_value})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    
    return JsonResponse({"error": "Invalid request"}, status=400)

@csrf_exempt  # Only use for testing; in production, use CSRF token validation
def average_daily_rate(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            data_value = f"${random.randint(2000, 20000)}"
            time.sleep(random.randint(2, 4))
            return JsonResponse({"data_value": data_value})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    
    return JsonResponse({"error": "Invalid request"}, status=400)