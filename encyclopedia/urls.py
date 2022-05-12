from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:name>", views.search, name="search"),
    path("new", views.new, name="new"),
    path("edit/<str:entry>", views.edit, name="edit"),
    path("rand", views.rand, name="rand")
]
