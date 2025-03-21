
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
import random
from datetime import datetime, timedelta
import time
import calendar
import threading
import concurrent.futures

from . import chart_data_library as cdl
from api_services import api_services
from . import utils
from api_services import enums

utility = utils.Utils()

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

@csrf_exempt  # Only use for testing; in production, use CSRF token validation
def age_group_segmentation_plotly(request):    
    def get_client_ids_for_arrivals(start_date, end_date):
        payload = {"Arrival From Day": start_date, "Arrival Until Before Day": end_date}
        bookings_ids = api_services.fetch_data(method="POST", endpoint="get_bookings_request", payload=payload)['Booking IDs']

        client_accounts = api_services.fetch_data(method="POST", endpoint="get_client_accounts_request", payload={})['Client Accounts']

        arriving_clients_ids = []
        for client_acc in client_accounts:
            if client_acc['Booking ID'] in bookings_ids:
                arriving_clients_ids.append(client_acc['Client ID'])

        return arriving_clients_ids

    def get_clients_with_ages(client_ids):
        payload = {'Client IDs': client_ids}
        clients_details = api_services.fetch_data(method="POST", endpoint="get_clients_details_request", payload=payload)['Clients']
        
        age_group = {"Child": 0, "Teenager": 0, "Adult": 0, "Elder": 0}

        # Define age group date ranges
        current_year = datetime.now().year
        child_date_range = [utility.date_to_code(f'01-01-{current_year - 12}'), utility.date_to_code(f'01-01-{current_year}')]  # Ages 0-12
        teen_date_range = [utility.date_to_code(f'01-01-{current_year - 19}'), utility.date_to_code(f'01-01-{current_year - 13}')]  # Ages 13-19
        adult_date_range = [utility.date_to_code(f'01-01-{current_year - 60}'), utility.date_to_code(f'01-01-{current_year - 20}')]  # Ages 20-60
        elder_date_range = [utility.date_to_code(f'01-01-{current_year - 100}')]

        for client in clients_details:
            birth_date = client['Birth Date']
            
            # Ensure birth_date is in a comparable format (integer or datetime)
            # For example, assuming utility.date_to_code returns a comparable integer (like YYMMDD)
            if isinstance(birth_date, int):
                if birth_date >= child_date_range[0] and birth_date <= child_date_range[1]:
                    age_group['Child'] += 1
                elif birth_date >= teen_date_range[0] and birth_date <= teen_date_range[1]:
                    age_group['Teenager'] += 1
                elif birth_date >= adult_date_range[0] and birth_date <= adult_date_range[1]:
                    age_group['Adult'] += 1
                elif birth_date >= elder_date_range[0]:
                    age_group['Elder'] += 1
            else:
                print(f"Invalid birth date format for client: {client['Client ID']}")

        return age_group

    if request.method == "POST":
        try:
            filterValues = json.loads(request.body)

            '''form_data = json.loads(filterValues['formData'])
            arriving_clients_ids = get_client_ids_for_arrivals(
                utility.date_to_code(utility.change_date_format(form_data['start_date'])),
                utility.date_to_code(utility.change_date_format(form_data['end_date'])),
                )
            data = get_clients_with_ages(arriving_clients_ids)'''

            data = {"Child": 10, "Adult": 15, "Middle Age": 12, "Elder": 18}

            chart_data = [{
                "x": list(data.keys()),
                "y": list(data.values()),
                "type": "bar",
                "marker": { "color": "#419fe3" }
            }]

            titles = {"x_axis_title": "Age Group", "y_axis_title": "Number"}

            cdl.chart_library.add_chart_data(filterValues["title"], filterValues["formData"], data)
            
            return JsonResponse({"data": chart_data, "titles": titles})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    
    return JsonResponse({"error": "Invalid request"}, status=400)

@csrf_exempt  # Only use for testing; in production, use CSRF token validation
def yearly_income_plotly(request):
    data = {}

    def get_bookings(year):
        bookings_per_month = {}

        def fetch_bookings_for_month(month):
            month_name = calendar.month_abbr[month]
            start_date = f"01-{month:02d}-{year}"
            last_day = calendar.monthrange(year, month)[1]
            end_date = f"{last_day:02d}-{month:02d}-{year}"

            payload = {"Departure From Day": utility.date_to_code(start_date), "Departure Until Before Day": utility.date_to_code(end_date)}
            bookings = api_services.fetch_data(method="POST", endpoint="get_bookings_request", payload=payload)['Booking IDs']
            
            return month_name, bookings

        with concurrent.futures.ThreadPoolExecutor() as executor:
            # Create a dictionary with month numbers (1 to 12) and API call futures
            futures = {month: executor.submit(fetch_bookings_for_month, month) for month in range(1, 13)}
            
            # Wait for all the API calls to complete and store results
            for month, future in futures.items():
                month_name, bookings = future.result()
                bookings_per_month[month_name] = bookings

        return bookings_per_month
    
    def calculate_monthly_income(bookings_per_month):
        payload = {
            "Include Transactions": True
        }
        clients_accounts = api_services.fetch_data(method="POST", endpoint="get_client_accounts_request", payload=payload)['Client Accounts']

        for month in bookings_per_month.keys():
            data[month] = 0

        for client_acc in clients_accounts:
            for month, bookings in bookings_per_month.items():
                if client_acc['Booking ID'] in bookings:
                    transactions = client_acc['Transactions']
                    for transaction in transactions:
                        data[month] += transaction['Amount']

    if request.method == "POST":
        try:
            filterValues = json.loads(request.body)

            form_data = json.loads(filterValues['formData'])

            '''year = int(form_data['selected_year'])
            bookings_per_month = get_bookings(year)
            calculate_monthly_income(bookings_per_month)'''

            data = {'Jan': 1000, 'Feb': 1500, 'Mar': 1200, 'Apr': 1800, 'May': 2000, 'Jun': 2200, 'Jul': 2500, 'Aug': 2800, 'Sep': 3000, 'Oct': 3200, 'Nov': 3500, 'Dec': 3800}

            chart_data = [{
                "x": list(data.keys()),
                "y": list(data.values()),
                "type": "line",
                "line": { "color": "lineColor", "width": 2 },
                "marker": { "size": 6, "color": "#419fe3" }  
            }]

            titles = {"x_axis_title": "Months", "y_axis_title": "Income"}
            cdl.chart_library.add_chart_data(filterValues["title"], filterValues["formData"], data)
            
            return JsonResponse({"data": chart_data, "titles": titles})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    
    return JsonResponse({"error": "Invalid request"}, status=400)

@csrf_exempt  # Only use for testing; in production, use CSRF token validation
def monthly_arrivals_plotly(request):
    data = {}

    def run_api(payload, month_name):
        bookings_dict = api_services.fetch_data(method="POST", endpoint="get_bookings_request", payload=payload)
        booking_count = len(bookings_dict['Booking IDs'])

        data[month_name] = booking_count

    if request.method == "POST":
        try:
            filterValues = json.loads(request.body)
            '''form_data = json.loads(filterValues['formData'])
            year = int(form_data['selected_year'])

            funcs = []

            for month in range(1, 13):
                month_name = calendar.month_abbr[month]
                start_date = f"01-{month:02d}-{year}"
                last_day = calendar.monthrange(int(form_data['selected_year']), month)[1]
                end_date = f"{last_day:02d}-{month:02d}-{year}"

                data[month_name] = 0

                payload = {
                    "Arrival From Day": utility.date_to_code(start_date),
                    "Arrival Until Before Day": utility.date_to_code(end_date)
                }

                # Pass the current value of month_name to the lambda
                funcs.append(lambda payload=payload, month_name=month_name: run_api(payload, month_name))

            threads = []

            for func in funcs:
                threads.append(threading.Thread(target=func))

            for thread in threads:
                thread.start()

            # Ensure threads are completed before returning response
            for thread in threads:
                thread.join()'''

            data = {
                "Jan": 120,
                "Feb": 90,
                "Mar": 130,
                "Apr": 100,
                "May": 80,
                "Jun": 150,
                "Jul": 140,
                "Aug": 110,
                "Sep": 70,
                "Oct": 95,
                "Nov": 125,
                "Dec": 60
            }

            chart_data = [{
                "y": list(data.keys()),
                "x": list(data.values()), 
                "type": "bar",
                "orientation": "h",
                "marker": { "color": "#419fe3"}
            }]

            cdl.chart_library.add_chart_data(filterValues["title"], filterValues["formData"], data)

            titles = {"x_axis_title": "Arrival Bookings", "y_axis_title": "Months"}
            additional_layout_config = {"bargap": 0.6}

            return JsonResponse({"data": chart_data, "titles": titles, "additional_layout_config": additional_layout_config})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    
    return JsonResponse({"error": "Invalid request"}, status=400)

@csrf_exempt
def arrivals_plotly(request):
    if request.method == "POST":
        try:
            filterValues = json.loads(request.body)
            '''form_data = json.loads(filterValues['formData'])
            payload = {
                'Arrival From Day': utility.date_to_code(utility.change_date_format(form_data['start_date'])),
                'Arrival Until Before Day': utility.date_to_code(utility.change_date_format(form_data['end_date'])),
            }
            bookings_dict = api_services.fetch_data(method="POST",endpoint="get_bookings_request", payload=payload)
            data = len(bookings_dict['Booking IDs'])'''
            
            time.sleep(random.randint(2, 4))
            data = 54

            cdl.chart_library.add_chart_data(filterValues["title"], filterValues["formData"], data)
            
            return JsonResponse({"data": data})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    
    return JsonResponse({"error": "Invalid request"}, status=400)

@csrf_exempt
def cancelled_bookings_plotly(request):
    if request.method == "POST":
        try:
            filterValues = json.loads(request.body)

            data = 54

            cdl.chart_library.add_chart_data(filterValues["title"], filterValues["formData"], data)
            
            return JsonResponse({"data": data})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    
    return JsonResponse({"error": "Invalid request"}, status=400)

@csrf_exempt
def departures_bookings_plotly(request):
    if request.method == "POST":
        try:
            filterValues = json.loads(request.body)
            
            '''form_data = json.loads(filterValues['formData'])
            payload = {
                'Departure From Day': utility.date_to_code(utility.change_date_format(form_data['start_date'])),
                'Departure Until Before Day': utility.date_to_code(utility.change_date_format(form_data['end_date'])),
            }
            bookings_dict = api_services.fetch_data(method="POST",endpoint="get_bookings_request", payload=payload)
            data = len(bookings_dict['Booking IDs'])'''

            data = 54

            cdl.chart_library.add_chart_data(filterValues["title"], filterValues["formData"], data)
            
            return JsonResponse({"data": data})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    
    return JsonResponse({"error": "Invalid request"}, status=400)

@csrf_exempt
def cancelled_bookings_percentage_plotly(request):
    if request.method == "POST":
        try:
            filterValues = json.loads(request.body)

            '''form_data = json.loads(filterValues['formData'])
            payload = {
                'Creation From Day': utility.date_to_code(utility.change_date_format(form_data['start_date'])),
                'Creation Until Before Day': utility.date_to_code(utility.change_date_format(form_data['end_date'])),
            }
            bookings_dict = api_services.fetch_data(method="POST",endpoint="get_bookings_request", payload=payload)
            total = len(bookings_dict['Booking IDs'])

            payload = {
                'Creation From Day': utility.date_to_code(utility.change_date_format(form_data['start_date'])),
                'Creation Until Before Day': utility.date_to_code(utility.change_date_format(form_data['end_date'])),
                'Booking Statuses': [enums.Enums.booking_status('Cancelled', 'desc')],
            }

            bookings_dict = api_services.fetch_data(method="POST",endpoint="get_bookings_request", payload=payload)
            canceled = len(bookings_dict['Booking IDs'])'''


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

            cdl.chart_library.add_chart_data(filterValues["title"], filterValues["formData"], {"Cancelled Bookings": canceled, "Total Bookings": total})
            
            return JsonResponse({"data": data, "additional_layout_config": additional_layout_config})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    
    return JsonResponse({"error": "Invalid request"}, status=400)

@csrf_exempt
def frequently_booked_units_plotly(request):
    data = {}

    def run_api(payload, unit_type_name):
        bookings_dict = api_services.fetch_data(method="POST", endpoint="get_bookings_request", payload=payload)
        booking_count = len(bookings_dict['Booking IDs'])

        data[unit_type_name] = booking_count
        
    if request.method == "POST":
        try:
            filterValues = json.loads(request.body)

            '''form_data = json.loads(filterValues['formData'])

            unit_type_dict = api_services.fetch_data(method="POST",endpoint="get_unit_type_categories_request", payload={})
            funcs = []
            for unit_type in unit_type_dict['Unit Type Categories']:
                unit_type_name = unit_type['Description'] 
                data[unit_type_name] = 0
                
                payload = {
                    "Creation From Day": utility.date_to_code(utility.change_date_format(form_data['start_date'])),
                    "Creation Until Before Day": utility.date_to_code(utility.change_date_format(form_data['end_date'])),
                    "Unit Type Category ID": unit_type['Unit Type Category ID'],
                }

                funcs.append(lambda payload=payload, unit_type_name=unit_type_name: run_api(payload, unit_type_name))

            threads = []

            for func in funcs:
                threads.append(threading.Thread(target=func))

            for thread in threads:
                thread.start()

            # Ensure threads are completed before returning response
            for thread in threads:
                thread.join()'''

            data = {"Deluxe Room": 120, "Suite": 80, "Standard Room": 150, "Penthouse": 50}
            chart_data = [{
                "labels": list(data.keys()),
                "values": list(data.values()),
                "type": "pie",
                "hole": 0.4,  # Creates the donut effect (0 = full pie, 0.4 = standard donut)
                "textinfo": "label+percent",
                "insidetextfont": { "color": "#fff" },
                "showlegend": False
            }]

            cdl.chart_library.add_chart_data(filterValues["title"], filterValues["formData"], data)

            sliceColors = chart_item_colors[:len(data)]
            chart_data[0]['marker'] = {"colors": sliceColors}

            additional_layout_config = {
                "legend": {
                    "font": { "size": 12, "color": "#fff" },
                    "bgcolor": "rgba(0, 0, 0, 0)",
                    "bordercolor": "#fff",
                    "borderwidth": 0
                }
            }
            
            return JsonResponse({"data": chart_data, "additional_layout_config": additional_layout_config})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    
    return JsonResponse({"error": "Invalid request"}, status=400)

@csrf_exempt
def member_general_guest_plotly(request):    
    def get_client_ids_for_arrivals(start_date, end_date):
        payload = {"Arrival From Day": start_date, "Arrival Until Before Day": end_date}
        bookings_ids = api_services.fetch_data(method="POST", endpoint="get_bookings_request", payload=payload)['Booking IDs']

        client_accounts = api_services.fetch_data(method="POST", endpoint="get_client_accounts_request", payload={})['Client Accounts']

        arriving_clients_ids = []
        for client_acc in client_accounts:
            if client_acc['Booking ID'] in bookings_ids:
                arriving_clients_ids.append(client_acc['Client ID'])

        return arriving_clients_ids
    
    def get_clients_with_membership(client_ids):
        payload = {'Client IDs': client_ids}
        clients_details = api_services.fetch_data(method="POST", endpoint="get_clients_details_request", payload=payload)['Clients']

        clients_memberships_counts = {"member": 0, "general": 0}
        for client in clients_details:
            if len(client['Membership List']) > 0:
                clients_memberships_counts['member'] += 1
            else:
                clients_memberships_counts['general'] += 1

        return clients_memberships_counts

    if request.method == "POST":
        try:
            filterValues = json.loads(request.body)

            '''form_data = json.loads(filterValues['formData'])
            arriving_clients_ids = get_client_ids_for_arrivals(
                utility.date_to_code(utility.change_date_format(form_data['start_date'])),
                utility.date_to_code(utility.change_date_format(form_data['end_date'])),
                )
            data = get_clients_with_membership(arriving_clients_ids)'''

            data = {"member": 30, "general": 156}

            chart_data = [
                {
                    "x": ["Guest Arrivals"],
                    "y": [data['member']],
                    "type": "bar",
                    "name": "member guest arrivals",
                    "marker": { "color": chart_item_colors[0] },
                    "hoverinfo": "y",
                    #"showlegend": True,
                },
                {
                    "x": ["Guest Arrivals"],
                    "y": [data['general']],
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

            cdl.chart_library.add_chart_data(filterValues["title"], filterValues["formData"], {"member guest arrivals": data['member'], "general guest arrivals": data['general']})
            
            return JsonResponse({"data": chart_data, "additional_layout_config": additional_layout_config})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    
    return JsonResponse({"error": "Invalid request"}, status=400)

@csrf_exempt
def occupancy_rate_plotly(request):
    def get_room_availability(start_date, end_date, unit_type_id):
        payload = {
            "Start Day": start_date,
            "End Day": end_date,
            "Blocking Booking Statuses":["A"],
            "Unit Type ID": unit_type_id
        }
        room_availability = api_services.fetch_data(method="POST",endpoint="get_room_availability_request", payload=payload)["Availabilities"]
        return room_availability
    
    def calculate_occupied_percentage(room_availability_data):
        total_available_days = 0
        total_room_days = 0

        for room in room_availability_data:
            # Length of "Is Available Online on Days" represents the number of days in the date range
            room_days = len(room['Is Available Online on Days'])
            total_room_days += room_days
            
            # Count the available days for the current room (sum of 1s in the availability array)
            available_days = sum(room['Is Available Online on Days'])
            total_available_days += available_days

        # Calculate the occupancy rate
        if total_room_days == 0:
            return 0  # Avoid division by zero if no rooms are available
        occupancy_rate = (total_available_days / total_room_days) * 100
        return occupancy_rate

    if request.method == "POST":
        try:
            filterValues = json.loads(request.body)

            '''form_data = json.loads(filterValues['formData'])
            selected_unit_id = int(form_data['selected_unit'])

            room_availability_data = get_room_availability(
                utility.date_to_code(utility.change_date_format(form_data['start_date'])),
                utility.date_to_code(utility.change_date_format(form_data['end_date'])),
                selected_unit_id
            )

            occupancy_rate = calculate_occupied_percentage(room_availability_data)'''

            occupancy_rate = 35

            chart_data = [
                {
                    "y": ["Rate"],
                    "x": [occupancy_rate],
                    "type": "bar",
                    "name": "Available",
                    "orientation": "h",
                    "textinfo": "label+percent",
                    "marker": { "color": chart_item_colors[1] },
                    "hoverinfo": "none",
                    "text": [f'{occupancy_rate}% available'],
                    "textposition": "inside",
                    "insidetextfont": { "color": '#fff' },
                    "showlegend": False,
                },
                {
                    "y": ["Rate"],
                    "x": [100-occupancy_rate],
                    "type": "bar",
                    "name": "Occupied",
                    "orientation": "h",
                    "marker": { "color": chart_item_colors[0] },
                    "hoverinfo": "none",
                    "text": [f'{100-occupancy_rate}% occupied'],
                    "textposition": "inside",
                    "insidetextfont": { "color": '#fff' },
                    "showlegend": False,
                },
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

            cdl.chart_library.add_chart_data(filterValues["title"], filterValues["formData"], {"Unit Type Name":"Standard","Occupancy Rate": f'{occupancy_rate}%'})
            
            return JsonResponse({"data": chart_data, "additional_layout_config": additional_layout_config})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    
    return JsonResponse({"error": "Invalid request"}, status=400)

@csrf_exempt
def average_daily_rate_plotly(request):
    def calculate_average_daily_rate(start_date, end_date, location_id):
        payload = {
            "Include Transactions": True
        }
        clients_accounts = api_services.fetch_data(method="POST", endpoint="get_client_accounts_request", payload=payload)['Client Accounts']

        total_revenue = 0

        date1_obj = datetime.strptime(start_date, '%d-%m-%Y')
        date2_obj = datetime.strptime(end_date, '%d-%m-%Y')

        delta = date2_obj - date1_obj
        total_days = delta.days + 1

        start_date_in_minutes = utility.convert_date_to_minutes(f'{start_date}, 00:00')
        end_date_in_minutes = utility.convert_date_to_minutes(f'{end_date}, 23:59')
        for client_account in clients_accounts:
            transactions = client_account['Transactions']
            for transaction in transactions:
                if start_date_in_minutes <= transaction['Transaction Minute'] <= end_date_in_minutes and transaction['Location ID'] == location_id:
                    total_revenue += transaction['Amount']

        adr_in_cents = total_revenue / total_days

        return round(adr_in_cents/100, 1)

    if request.method == "POST":
        try:
            filterValues = json.loads(request.body)

            '''form_data = json.loads(filterValues['formData'])
            location_id = int(form_data['selected_location'])

            data = calculate_average_daily_rate(
                utility.change_date_format(form_data['start_date']),
                utility.change_date_format(form_data['end_date']),
                location_id
            )'''

            data = 82557
            
            cdl.chart_library.add_chart_data(filterValues["title"], filterValues["formData"], f'${data}')

            return JsonResponse({"data": f'${data}'})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    
    return JsonResponse({"error": "Invalid request"}, status=400)

@csrf_exempt
def client_birthdays_plotly(request):
    def get_clients_within_date_range(start_date, end_date):
        payload = {
                   "Birthday Month Day From": utility.date_to_month_code(utility.change_date_format(start_date)),
                   "Birthday Month Day Until": utility.date_to_month_code(utility.change_date_format(end_date)),
                   }
        clients = api_services.fetch_data(method="POST", endpoint="get_clients_request", payload={})
        client_ids = [client["Client ID"] for client in clients['Clients']]

        return client_ids    

    def get_client_birthdays(clients_ids):
        clients_with_birthdays = []

        payload = {"Client IDs": clients_ids}
        clients = api_services.fetch_data(method="POST", endpoint="get_clients_details_request", payload=payload)['Clients']

        if len(clients) == 0: return

        clients.sort(key=lambda client: client["Birth Date"])

        for client in clients:
            if (client["First Name"] == "" and client["Surname"] == "") or client["Birth Date"] == 0: continue
            clients_with_birthdays.append({
                "firstName": client["First Name"],
                "lastName": client["Surname"],
                "birthday": utility.code_to_date(client["Birth Date"]),
            })

        return clients_with_birthdays

    if request.method == "POST":
        try:
            filterValues = json.loads(request.body)

            '''form_data = json.loads(filterValues['formData'])
            clients_ids = get_clients_within_date_range(form_data['start_date'], form_data['end_date'])
            data = get_client_birthdays(clients_ids)'''

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

            cdl.chart_library.add_chart_data(filterValues["title"], filterValues["formData"], data)
            return JsonResponse({"data": data})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    
    return JsonResponse({"error": "Invalid request"}, status=400)