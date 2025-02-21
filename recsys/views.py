from django.shortcuts import render, get_object_or_404, redirect
from .models import Farmer, Market, Personal, Product
from django.http import HttpResponse
from .forms import FarmerForm, MarketForm, PersonalForm, ProductForm
from django.db.models import Count

def index(request):
    return HttpResponse("testing", request)                                                       
# Create your views here.
from django.shortcuts import render
from .models import Farmer, Market, Personal, Product
from geopy.distance import geodesic
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse


'''#This will give the best matches for both the market and the personal buyer, we can devide it later
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
        return JsonResponse({"error": "Farmer not found, the id may be invalid."}, status = 404)'''

#THE SCALES
# ┌───────────────────────────┬───────────────────┬───────────────────┐
# │       Criteria            │ Personal Buyer    │ Market Buyer      │
# ├───────────────────────────┼───────────────────┼───────────────────┤
# │ Product Match             │ 0.3 (30%)         │ 0.2 (20%)         │
# │ Order Quantity            │ 0.1 (10%)         │ 0.35 (30%)        │
# │ Distance                  │ 0.25 (25%)        │ 0.15 (10%)        │
# │ Buyer Type Match          │ 0.15 (15%)        │ 0.05 (5%)         │
# │ Payment Terms Match       │ 0.1 (10%)         │ 0.1 (10%)         │
# └───────────────────────────┴───────────────────┴───────────────────┘

def score_productmatch(farmer, buyer):
    farmer_products = set(farmer.products.values_list('id', flat=True))
    buyer_products = set(buyer.preferred_products.values_list('id', flat=True))

    matched_products = farmer_products.intersection(buyer_products)
    if((matched_products == 0) or (not farmer_products)):
        return -9999

    return len(matched_products)/len(farmer_products) #returns a ratio of how much matches

def score_quantity_match(farmer, buyer):
    farmer_preferred = farmer.min_quantity_order
    buyer_preferred = buyer.preferred_order_quantity

    score = (buyer_preferred - farmer_preferred) / farmer_preferred

    if score<0:
        return 0
    if score > 2 * farmer_preferred:
        return 1
    else:
        return score

def score_distance(farmer, buyer):
    farmer_location = (farmer.latitude, farmer.longitude)
    buyer_location = (buyer.latitude, buyer.longitude)

    if not buyer.latitude or not buyer.longitude:#in case invalid location
        return 0  

    distance = geodesic(farmer_location, buyer_location).km

    if distance <= farmer.delivery_region:
        return 1
    elif buyer.can_arrange_transport:
        return 0.8
    else:
        return max(0, 1 - (distance / (farmer.delivery_region * 2))) 
    
def score_buyer_type(farmer, buyer):
    if farmer.buyer_choice == 'both':
        return 1
    if farmer.buyer_choice == 'personal' and isinstance(buyer, Personal):
        return 1
    if farmer.buyer_choice == 'market' and isinstance(buyer, Market):
        return 1
    return 0

def score_payment_terms(farmer, buyer):
    if farmer.payment_terms == 'any' or buyer.payment_terms == 'any':
        return 1  
    return 1 if farmer.payment_terms == buyer.payment_terms else -999


def calculate_market_buyer_score(farmer, buyer):
    weights = {
        "product": 0.2,
        "quantity": 0.35,
        "distance": 0.15,
        "buyer_type": 0.05,
        "payment": 0.1,
    }

    score = score_productmatch(farmer, buyer) * weights['product']
    score += score_buyer_type(farmer, buyer) * weights['buyer_type']
    score += score_distance(farmer, buyer) * weights['distance']
    score += score_payment_terms(farmer, buyer) * weights['payment']
    score += score_quantity_match(farmer, buyer) * weights['quantity']

    return score

def calculate_personal_buyer_score(farmer, buyer):

    weights = {
        "product": 0.3,      
        "quantity": 0.1,     
        "distance": 0.25,    
        "buyer_type": 0.15,  
        "payment": 0.1,      
    }

    score = score_productmatch(farmer, buyer) * weights['product']
    score += score_buyer_type(farmer, buyer) * weights['buyer_type']
    score += score_distance(farmer, buyer) * weights['distance']
    score += score_payment_terms(farmer, buyer) * weights['payment']
    score += score_quantity_match(farmer, buyer) * weights['quantity']

    return score

def match_farmer_to_market(request, farmer_id):
    farmer = get_object_or_404(Farmer, id=farmer_id)
    buyers = Market.objects.all()
    
    buyer_scores = [(buyer, calculate_market_buyer_score(farmer, buyer)) for buyer in buyers]
    buyer_scores.sort(key=lambda item: item[1], reverse=True)  # Sort by highest score

    recommended = buyer_scores[:3]  # Get top 3 matches

    return render(request, 'recsys/recommended_matches.html', {
        'instance': farmer,
        'recommended': recommended,
    })

def match_farmer_to_personal(request, farmer_id):
    farmer = get_object_or_404(Farmer, id=farmer_id)
    buyers = Personal.objects.all()
    
    buyer_scores = [(buyer, calculate_personal_buyer_score(farmer, buyer)) for buyer in buyers]
    buyer_scores.sort(key=lambda item: item[1], reverse=True)  # Sort by highest score

    recommended = buyer_scores[:3]  # Get top 3 matches

    return render(request, 'recsys/recommended_matches.html', {
        'instance': farmer,
        'recommended': recommended,
    })


def add_farmer(request):
    if request.method == "POST":
        form = FarmerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')  # Redirect to a success page
    else:
        form = FarmerForm()
    return render(request, 'recsys/add_farmer.html', {'form': form})

def add_market(request):
    if request.method == "POST":
        form = MarketForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')  # Redirect to a success page
    else:
        form = MarketForm()
    return render(request, 'recsys/add_market.html', {'form': form})

def add_personal(request):
    if request.method == "POST":
        form = PersonalForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')  # Redirect to a success page
    else:
        form = PersonalForm()
    return render(request, 'recsys/add_personal.html', {'form': form})

def add_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')  # Redirect to a success page
    else:
        form = ProductForm()
    return render(request, 'recsys/add_product.html', {'form': form})


def main_page(request):
    # Get top 5 for each model (adjust based on your recommendation logic)
    top_farmers = Farmer.objects.all()[:5]
    top_markets = Market.objects.all()[:5]
    top_personals = Personal.objects.all()[:5]
    top_products = Product.objects.all()[:5]

    return render(request, 'recsys/main_page.html', {
        'top_farmers': top_farmers,
        'top_markets': top_markets,
        'top_personals': top_personals,
        'top_products': top_products
    })

def match_market_to_farmers(request, market_id):
    market = get_object_or_404(Market, id=market_id)
    farmers = Farmer.objects.all()

    farmer_scores = [(farmer, calculate_market_buyer_score(farmer, market)) for farmer in farmers]
    farmer_scores.sort(key=lambda item: item[1], reverse=True)  

    recommended = farmer_scores[:3]  

    return render(request, 'recsys/recommended_matches.html', {
        'instance': market,
        'recommended': recommended,
    })


# ✅ Match a personal buyer to farmers
def match_personal_to_farmers(request, personal_id):
    personal_buyer = get_object_or_404(Personal, id=personal_id)
    farmers = Farmer.objects.all()

    farmer_scores = [(farmer, calculate_personal_buyer_score(farmer, personal_buyer)) for farmer in farmers]
    farmer_scores.sort(key=lambda item: item[1], reverse=True)  

    recommended = farmer_scores[:3]  

    return render(request, 'recsys/recommended_matches.html', {
        'instance': personal_buyer,
        'recommended': recommended,
    })