from django.urls import path
from . import views

urlpatterns = [
    path('', views.SavedReportListCreateView.as_view(), name='savedreport-list'),
    path('<int:pk>/', views.SavedReportDetailView.as_view(), name='savedreport-detail'),
    path('pdf/', views.generate_pdf_report, name='report-pdf'),
]
