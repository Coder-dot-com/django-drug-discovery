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
from . import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', views.home, name="home"),
    path('privacy_policy', views.privacy_policy, name="privacy_policy"),
    path('terms_and_conditions', views.terms_and_conditions, name="terms_and_conditions"),
  
    
    path('accounts/', include('accounts.urls')),
    path('dashboard/', include('dashboard.urls')),

    path('generate/', include('generate_molecules.urls')),
    path('render/', include('render_molecules.urls')),
    path('reports/', include('reports.urls')),

    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)