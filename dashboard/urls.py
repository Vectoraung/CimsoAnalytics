from django.urls import path
from . import views
from . import chart_data_retriever
from . import generate_chart_report

urlpatterns = [
    path('booking-dashboard/', views.booking_dashboard_view, name='booking_dashboard'),
    path('get-arrivals-count/', chart_data_retriever.get_arrivals_count, name='get_arrivals_count'),
    path('get-departures-count/', chart_data_retriever.get_departures_count, name='get_departures_count'),
    path('get-cancelled-bookings-count/', chart_data_retriever.get_cancelled_bookings_count, name='get_cancelled_bookings_count'),
    path('get-cancelled-bookings-percentage/', chart_data_retriever.get_cancelled_bookings_percentage, name='get_cancelled_bookings_percentage'),
    path('booking-arrivals-yearly/', chart_data_retriever.booking_arrivals_yearly, name='booking_arrivals_yearly'),
    path('client-birthdays/', chart_data_retriever.client_birthdays, name='client_birthdays'),
    path('member-guest-arrivals-count/', chart_data_retriever.member_guest_arrivals_count, name='member_guest_arrivals_count'),
    path('general-guest-arrivals-count/', chart_data_retriever.general_guest_arrivals_count, name='general_guest_arrivals_count'),
    path('most-frequently-units/', chart_data_retriever.most_frequently_units, name='most_frequently_units'),
    path('age-group-segmentation/', chart_data_retriever.age_group_segmentation, name='age_group_segmentation'),
    path('occupancy-rate/', chart_data_retriever.occupancy_rate, name='occupancy_rate'),
    path('average-daily-rate/', chart_data_retriever.average_daily_rate, name='average_daily_rate'),

    path('generate-report/', generate_chart_report.generate_report, name='generate_report'),
]
