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
from django.conf.urls.static import static

urlpatterns = [
    path('list_of_requests/', views.list_of_requests, name="list_of_requests"),
    path('molecules/<uuid>', views.render_molecules, name="render_molecules"),
   
    path('filter_molecules/<uuid>', views.filter_molecules, name="filter_molecules"),
    path('filter_molecules_htmx/<uuid>', views_htmx.filter_molecules_htmx, name="filter_molecules_htmx"),
    path('load_reports_list_htmx/', views_htmx.load_reports_list_htmx, name="load_reports_list_htmx"),


]