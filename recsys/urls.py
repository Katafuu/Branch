from django.urls import path

from . import views

urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('add_farmer/', views.add_farmer, name='add_farmer'),
    path('add_product/', views.add_product, name='add_product'),
    path('add_personal/', views.add_personal, name='add_personal'),
    path('add_market/', views.add_market, name='add_market'),
    path('market_farmer/<int:market_id>/', views.match_market_to_farmers, name='match_market_to_farmers'),
    path('personal_farmer/<int:personal_id>/', views.match_personal_to_farmers, name='match_personal_to_farmers'),
    path("farmer_personal/<int:farmer_id>/", views.match_farmer_to_personal, name = "match_farmer_to_personal"),
    path("farmer_market/<int:farmer_id>/", views.match_farmer_to_market, name = "match_farmer_to_market"),
]