from django.urls import path
from medication_log import views

urlpatterns = [
    path("", views.index),
    path("new/", views.new),
    path("edit/<int:id>", views.edit),
    path("update/<int:id>", views.update),
    path("delete/<int:id>", views.destroy),
]
