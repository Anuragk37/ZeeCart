from django.urls import path
from .import views

urlpatterns = [
    path('dashboard/',views.dashboard, name='dashboard'),
    path('admin-login/',views.admin_login, name='admin_login'),
    path('admin_logout',views.admin_logout, name='admin_logout'),

    path('sales-report/',views.sales_report, name='sales_report'),
    path('date-filter/',views.date_filter, name='date_filter'),

    path('sales-report-pdf/<str:time_period>', views.sales_report_pdf, name='sales_report_pdf'),
    path('excel_report/<str:time_period>', views.excel_report, name='excel_report'),

   
]