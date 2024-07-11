from django.contrib import admin
from django.urls import path
from . import views, views_htmx, views_from_target

urlpatterns = [
    path("molecules_or_target/", views_htmx.molecules_or_target, name="molecules_or_target"),
    path("molecules_or_target_post/", views_htmx.molecules_or_target_post, name="molecules_or_target_post"),
    path("from_molecules_post/<uuid>", views_htmx.from_molecules_post, name="from_molecules_post"),

    
    path("handle_target_organism_post/<uuid>", views_from_target.handle_target_organism_post, name="handle_target_organism_post"),    
    path("handle_disease_target_post/<uuid>", views_from_target.handle_disease_target_post, name="handle_disease_target_post"),
    path("handle_target_post/<uuid>", views_from_target.handle_target_post, name="handle_target_post"),
    path("molecule_count/<uuid>", views_from_target.molecule_count, name="molecule_count"),
    
    path("restart_creation_flow/", views_htmx.restart_creation_flow, name="restart_creation_flow"),
    path("create_molecule/<uuid>", views_htmx.create_molecule, name="create_molecule"),

    path("poll_for_request_completion/<uuid>", views_htmx.poll_for_request_completion, name="poll_for_request_completion"),

    
] 
