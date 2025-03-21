from django.urls import path
from . import views
from . import chart_data_retriever
from . import generate_chart_report
from . import get_charts_data_plotly
from . import report_generator_ai

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

    path('overwhelming-view-plotly', views.booking_dashboard_view_plotly, name='booking_dashboard_plotly'),
    path('', views.booking_dashboard_view_plotly, name='booking_dashboard_plotly'),
    path('single-chart-view-plotly/', views.booking_dashboard_view_single_chart_plotly, name='booking_dashboard_view_single_chart_plotly'),
    #path('booking-dashboard-plotly/', views.booking_dashboard_view_plotly, name='booking_dashboard_plotly'),
    path("arrivals-plotly/", get_charts_data_plotly.arrivals_plotly, name="arrivals_plotly"),
    path("departures-bookings-plotly/", get_charts_data_plotly.departures_bookings_plotly, name="departures_bookings_plotly"),
    path("cancelled-bookings-percentage-plotly/", get_charts_data_plotly.cancelled_bookings_percentage_plotly, name="cancelled_bookings_percentage_plotly"),
    path("age-group-segmentation-plotly/", get_charts_data_plotly.age_group_segmentation_plotly, name="age_group_segmentation_plotly"),
    path("yearly-income-plotly/", get_charts_data_plotly.yearly_income_plotly, name="yearly_income_plotly"),
    path("monthly-arrivals-plotly/", get_charts_data_plotly.monthly_arrivals_plotly, name="monthly_arrivals_plotly"),
    path("frequently-booked-units-plotly/", get_charts_data_plotly.frequently_booked_units_plotly, name="frequently_booked_units_plotly"),
    path("member-general-guest-plotly/", get_charts_data_plotly.member_general_guest_plotly, name="member_general_guest_plotly"),
    path("occupancy-rate-plotly/", get_charts_data_plotly.occupancy_rate_plotly, name="occupancy_rate_plotly"),
    path("average-daily-rate-plotly/", get_charts_data_plotly.average_daily_rate_plotly, name="average_daily_rate_plotly"),
    path("client-birthdays-plotly/", get_charts_data_plotly.client_birthdays_plotly, name="client_birthdays_plotly"),
    path("generate-report-plotly/", report_generator_ai.generate_report, name="generate_report_plotly"),
]
