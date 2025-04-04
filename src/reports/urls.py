"""
URL configuration for drug_discovery project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views, views_htmx

urlpatterns = [
    path('list_of_reports/', views.list_of_reports, name="list_of_reports"),
    
    path('view_report/<uuid>', views.view_report, name="view_report"),

    path('export_report_molecules_csv/<uuid>', views.export_report_molecules_csv, name="export_report_molecules_csv"),

    path('create_report_htmx/', views_htmx.create_report_htmx, name="create_report_htmx"),
    path('create_report_molecules_display_htmx/', views_htmx.create_report_molecules_display_htmx, name="create_report_molecules_display_htmx"),

    
    path('remove_molecule_from_report_htmx/<molecule_uuid>/<report_uuid>', views_htmx.remove_molecule_from_report_htmx, name="remove_molecule_from_report_htmx"),

    path('add_all_molecules_to_report_htmx/', views_htmx.add_all_molecules_to_report_htmx, name="add_all_molecules_to_report_htmx"),

    

]