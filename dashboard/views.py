from django.shortcuts import render


# Create your views here.
def booking_dashboard_view_plotly(request):
    charts = {
        "chart1":{
                "chartId": "chart1",
                "title": "Arrivals within period",
                "data_url": "/arrivals-plotly/",
                "type": "single_value",
                "filters": [
                    {
                        "name": "start_date",
                        "type": "date",
                        "label": "Start Date",
                        "default": "2024-01-01"
                    },
                    {
                        "name": "end_date",
                        "type": "date",
                        "label": "End Date",
                        "default": "2024-12-31"
                    },
                ],
        },
        "chart2":{
                "chartId": "chart2",
                "title": "Departure bookings within period",
                "data_url": "/departures-bookings-plotly/",
                "type": "single_value",
                "filters": [
                    {
                        "name": "start_date",
                        "type": "date",
                        "label": "Start Date",
                        "default": "2024-01-01"
                    },
                    {
                        "name": "end_date",
                        "type": "date",
                        "label": "End Date",
                        "default": "2024-12-31"
                    },
                ],
        },
        "chart3":{
                "chartId": "chart3",
                "title": "Cancelled bookings percentage within period",
                "data_url": "/cancelled-bookings-percentage-plotly/",
                "type": "chart",
                "filters": [
                    {
                        "name": "start_date",
                        "type": "date",
                        "label": "Start Date",
                        "default": "2024-01-01"
                    },
                    {
                        "name": "end_date",
                        "type": "date",
                        "label": "End Date",
                        "default": "2024-12-31"
                    },
                ],
        },
        "chart4":{
                "chartId": "chart4",
                "title": "Monthly Arrival Bookings",
                "data_url": "/monthly-arrivals-plotly/",
                "type": "chart",
                "filters": [
                    {
                        "name": "selected_year",
                        "type": "radio",
                        "label": "Selected Year:",
                        "options": [
                            {"value": "2020", "label": "2020"},
                            {"value": "2021", "label": "2021"},
                            {"value": "2022", "label": "2022"},
                            {"value": "2023", "label": "2023"},
                            {"value": "2024", "label": "2024"},
                            {"value": "2025", "label": "2025"},
                            {"value": "2026", "label": "2026"}
                        ],
                        "default": "2025"
                    }
                ]
        },
        "chart5":{
                "chartId": "chart5",
                "title": "Yearly Income",
                "data_url": "/yearly-income-plotly/",
                "type": "chart",
                "filters": [
                    {
                        "name": "selected_year",
                        "type": "radio",
                        "label": "Selected Year:",
                        "options": [
                            {"value": "2020", "label": "2020"},
                            {"value": "2021", "label": "2021"},
                            {"value": "2022", "label": "2022"},
                            {"value": "2023", "label": "2023"},
                            {"value": "2024", "label": "2024"},
                            {"value": "2025", "label": "2025"},
                            {"value": "2026", "label": "2026"}
                        ],
                        "default": "2025"
                    }
                ]
        },
        "chart6":{
                "chartId": "chart6",
                "title": "Frequently Booked Units",
                "data_url": "/frequently-booked-units-plotly/",
                "type": "chart",
                "filters": [
                    {
                        "name": "start_date",
                        "type": "date",
                        "label": "Start Date",
                        "default": "2024-01-01"
                    },
                    {
                        "name": "end_date",
                        "type": "date",
                        "label": "End Date",
                        "default": "2024-12-31"
                    },
                ],
        },
        "chart7":{
                "chartId": "chart7",
                "title": "Age group Segmentation",
                "data_url": "/age-group-segmentation-plotly/",
                "type": "chart",
                "filters": [
                    {
                        "name": "start_date",
                        "type": "date",
                        "label": "Start Date",
                        "default": "2024-01-01"
                    },
                    {
                        "name": "end_date",
                        "type": "date",
                        "label": "End Date",
                        "default": "2024-12-31"
                    },
                ],
        },
        "chart8":{
                "chartId": "chart8",
                "title": "Client birthdays",
                "data_url": "/client-birthdays-plotly/",
                "type": "table",
                "filters": [
                    {
                        "name": "start_date",
                        "type": "date",
                        "label": "Start Date",
                        "default": "2024-01-01"
                    },
                    {
                        "name": "end_date",
                        "type": "date",
                        "label": "End Date",
                        "default": "2024-12-31"
                    },
                ],
        },
        "chart9":{
                "chartId": "chart9",
                "title": "Member Guests and General Guests",
                "data_url": "/member-general-guest-plotly/",
                "type": "chart",
                "filters": [
                    {
                        "name": "start_date",
                        "type": "date",
                        "label": "Start Date",
                        "default": "2024-01-01"
                    },
                    {
                        "name": "end_date",
                        "type": "date",
                        "label": "End Date",
                        "default": "2024-12-31"
                    },
                ],
        },
        "chart10":{
                "chartId": "chart10",
                "title": "Occupancy Rate",
                "data_url": "/occupancy-rate-plotly/",
                "type": "chart",
                "filters": [
                    {
                        "name": "start_date",
                        "type": "date",
                        "label": "Start Date",
                        "default": "2024-01-01"
                    },
                    {
                        "name": "end_date",
                        "type": "date",
                        "label": "End Date",
                        "default": "2024-12-31"
                    },
                ],
        },
        "chart11":{
                "chartId": "chart11",
                "title": "Average Daily Rate",
                "data_url": "/average-daily-rate-plotly/",
                "type": "single_value",
                "filters": [
                    {
                        "name": "start_date",
                        "type": "date",
                        "label": "Start Date",
                        "default": "2024-01-01"
                    },
                    {
                        "name": "end_date",
                        "type": "date",
                        "label": "End Date",
                        "default": "2024-12-31"
                    },
                ],
        },
        
    }

    return render(request, 'dashboard/booking_dashboard_plotly.html', {
        "charts": charts,})

def booking_dashboard_view(request):
    context = {
        "charts": {
            "chart1": {
                "js_function":"singleValueChart1",
                "request_url": "get-arrivals-count",
                "report_request_url": "arrivals-count-report",
                "chart_id": "chartbox1",
                "chart_title": "Arrivals",
                "filters": [
                    {"type": "datepicker",
                    "label": "From Date",
                    "name": "from-date",
                    "default_value": "03-03-2025",
                    },
                    {"type": "datepicker",
                    "label": "Until Date",
                    "name": "until-date",
                    "default_value": "05-03-2025",
                    },
                ],
            },
            "chart2": {
                "chart_id": "chartbox2",
                "chart_title": "Canceled Bookings",
                "js_function":"singleValueChart1",
                "request_url": "get-cancelled-bookings-count",
                "filters": [
                    {"type": "datepicker",
                    "label": "From Date",
                    "name": "from-date",
                    "default_value": "03-03-2025",
                    },
                    {"type": "datepicker",
                    "label": "Until Date",
                    "name": "until-date",
                    "default_value": "05-03-2025",
                    },
                ],
                },
            "chart3": {
                "chart_id": "chartbox3",
                "chart_title": "Departures",
                "js_function":"singleValueChart1",
                "request_url": "get-departures-count",
                "filters":[
                    {"type": "datepicker",
                    "label": "From Date",
                    "name": "from-date",
                    "default_value": "03-03-2025",
                    },
                    {"type": "datepicker",
                    "label": "Until Date",
                    "name": "until-date",
                    "default_value": "05-03-2025",
                    },
                ]
                },
            "chart4": {
                "chart_id": "chartbox4",
                "chart_title": "Canceled Bookings Percentage",
                "js_function":"singleValueChart1",
                "request_url": "get-cancelled-bookings-percentage",
                "filters":[
                    {"type": "datepicker",
                    "label": "From Date",
                    "name": "from-date",
                    "default_value": "03-03-2025",
                    },
                    {"type": "datepicker",
                    "label": "Until Date",
                    "name": "until-date",
                    "default_value": "05-03-2025",
                    },
                ],
                },
            "chart5": {
                "chart_id": "chartbox5",
                "chart_title": "Arrivals by Year",
                "js_function":"renderBookingsChart",
                "request_url": "booking-arrivals-yearly",
                "filters":[
                    {
                        "type": "radio",
                        "name": "year",
                        "label": "Year",
                        "options": [
                        {
                            "value": "2022",
                            "label": "2022"
                        },
                        {
                            "value": "2023",
                            "label": "2023"
                        },
                        {
                            "value": "2024",
                            "label": "2024"
                        },
                        {
                            "value": "2025",
                            "label": "2025"
                        },
                        {
                            "value": "2026",
                            "label": "2026"
                        },
                        ],
                        "default_value": "2025",
                    },
                ]
                },
            "chart6": {
                "chart_id": "chartbox6",
                "chart_title": "Income by Month and Year",
                "js_function":"renderYearlyChart",
                },
            "chart7": {
                "chart_id": "chartbox7",
                "chart_title": "Client Birthdays",
                "js_function":"clientBirthdaysChart",
                "request_url": "client-birthdays",
                "filters":[
                    {"type": "datepicker",
                    "label": "From Date",
                    "name": "from-date",
                    "default_value": "01-03-2025",
                    },
                    {"type": "datepicker",
                    "label": "Until Date",
                    "name": "until-date",
                    "default_value": "31-03-2025",
                    },
                ],
                },
            "chart8": {
                "chart_id": "chartbox8",
                "chart_title": "Member Guests",
                "js_function":"singleValueChart1",
                "request_url": "member-guest-arrivals-count",
                "filters":[
                    {"type": "datepicker",
                    "label": "From Date",
                    "name": "from-date",
                    "default_value": "01-03-2025",
                    },
                    {"type": "datepicker",
                    "label": "Until Date",
                    "name": "until-date",
                    "default_value": "31-03-2025",
                    },
                ],
                },
            "chart9": {
                "chart_id": "chartbox9",
                "chart_title": "General Guests",
                "js_function":"singleValueChart1",
                "request_url": "general-guest-arrivals-count",
                "filters":[
                    {"type": "datepicker",
                    "label": "From Date",
                    "name": "from-date",
                    "default_value": "01-03-2025",
                    },
                    {"type": "datepicker",
                    "label": "Until Date",
                    "name": "until-date",
                    "default_value": "31-03-2025",
                    },
                ],
                },
            "chart10": {
                "chart_id": "chartbox10",
                "chart_title": "Age Group Segmentation",
                "js_function":"ageGroupSegmentationChart",
                "request_url": "age-group-segmentation",
                },
            "chart11": {
                "chart_id": "chartbox11",
                "chart_title": "Frequently Booked Units",
                "js_function":"frequentlyBookedUnitsCharts",
                "request_url": "most-frequently-units",
                },
            "chart12": {
                "chart_id": "chartbox12",
                "chart_title": "Occupancy Rate",
                "js_function":"singleValueChart1",
                "request_url": "occupancy-rate",
                "filters":[
                    {"type": "datepicker",
                    "label": "From Date",
                    "name": "from-date",
                    "default_value": "01-03-2025",
                    },
                    {"type": "datepicker",
                    "label": "Until Date",
                    "name": "until-date",
                    "default_value": "31-03-2025",
                    },
                ],
                },
            "chart13": {
                "chart_id": "chartbox13",
                "chart_title": "Average Daily Rate",
                "request_url": "average-daily-rate",
                "js_function":"singleValueChart1",
                "filters":[
                    {"type": "datepicker",
                    "label": "From Date",
                    "name": "from-date",
                    "default_value": "01-03-2025",
                    },
                    {"type": "datepicker",
                    "label": "Until Date",
                    "name": "until-date",
                    "default_value": "31-03-2025",
                    },
                ],
                },
            }
        }
    
    return render(request, 'dashboard/booking_dashboard.html', context)