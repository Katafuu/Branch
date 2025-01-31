from django.shortcuts import render
from .models import Farmer, Market, Personal
from geopy.distance import geodesic
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
def match_buyer_farmer(farmer):
    #first, with the location

    farmer_location = (farmer.latitude, farmer.longitude)

    final_buyers = list(Personal.objects.all()) + list(Market.objects.all)

    matched_buyers_by_distance = []

    for buyer in final_buyers:
        buyer_location = (buyer.latitude, buyer.longitude)
        distance = geodesic(farmer_location, buyer_location).km
        matched_buyers_by_distance.append((buyer, distance))
    
    matched_buyers_by_distance.sort(key=lambda x:x[1])


#an api that will send the json response of the results
@csrf_exempt
def get_matched_buyer(request, farmed_id):
    try:
        farmer = Farmer.objects.get(id=farmed_id)
        matched_buyers = match_buyer_farmer(farmer)
        response =[
            {"buyer_name": buyer.name, "distance_km": distance}
            for buyer, distance, in matched_buyers
        ]

        return JsonResponse({"farmer": farmer.first_name, "matches": response}, safe=False)
    
    except Farmer.DoesNotExist:
        return JsonResponse({"error": "Farmer not found, the id may be invalid."}, status = 404)