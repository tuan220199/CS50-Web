from django.urls import path

from . import views

app_name = "encyclopedia"

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("search", views.search, name="search"),
    path("create_new", views.create_new, name="create_new"),
    path("edit", views.edit, name="edit"),
    path("edit_result", views.edit_result, name="edit_result"),
    path("random_page", views.random_page, name="random_page")
]
