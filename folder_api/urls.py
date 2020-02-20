from django.urls import path

from . import views

urlpatterns = [
    path('initialize', views.index), # initialize data
    path('resources/<resource_id>', views.resource),
    path('folders/', views.folder),
    path('questions/<question_id>', views.question),
]