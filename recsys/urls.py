from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name='index'),
    path("reccpersonal/<int:farmer_id>/", views.match_farmer_to_personal, name = "match_farmer_to_personal"),
    path("reccmarket/<int:farmer_id>/", views.match_farmer_to_market, name = "match_farmer_to_market"),
]