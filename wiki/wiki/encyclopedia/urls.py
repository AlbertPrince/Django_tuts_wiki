from django.urls import path

from . import views

# app_name = "wiki"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("random/", views.random_entry, name="random_entry"),
    path("create/", views.create_entry, name="create"),
    path("edit/<str:title>", views.edit_entry, name="edit"),
    path('search/', views.search, name='search')
]
