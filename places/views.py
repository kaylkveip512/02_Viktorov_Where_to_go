from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_GET
import random
from .forms import PlaceForm
from datetime import datetime

def home(request):
    return render(request, 'home.html')

def place_list(request):
    places = request.session.get('places', [])
    return render(request, 'place_list.html', {'places': places})

def place_details(request, pk):
    places = request.session.get('places', [])
    try:
        place = places[int(pk)]
        place_type_display = dict(PlaceForm.PLACE_TYPES).get(place['place_type'], place['place_type'])
        place['place_type_display'] = place_type_display
    except (IndexError, ValueError):
        return render(request, '404.html', status=404)
    return render(request, 'place_detail.html', {'place': place})

def add_place(request):
    if request.method == 'POST':
        form = PlaceForm(request.POST)
        if form.is_valid():
            places = request.session.get('places', [])
            new_place = {
                'id': len(places),
                'name': form.cleaned_data['name'],
                'description': form.cleaned_data['description'],
                'place_type': form.cleaned_data['place_type'],
                'place_type_display': dict(form.PLACE_TYPES).get(form.cleaned_data['place_type']),
                'place_type': form.cleaned_data['place_type'],
                'location': form.cleaned_data['location'],
                'rating': form.cleaned_data['rating'],
                'created_at':  datetime.now().strftime('%d.%m.%Y'),
            }
            places.append(new_place)
            request.session['places'] = places
            return redirect('places:place_list')
    else:
        form = PlaceForm()
    return render(request, 'add_place.html', {'form': form})

@require_GET
def random_place(request):
    places = request.session.get('places', [])
    if not places:
        return JsonResponse({'error': 'No places available'})
    
    weights = [place['rating'] for place in places]
    selected_place = random.choices(places, weights=weights, k=1)[0]
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'name': selected_place['name'],
            'description': selected_place['description'],
            'type': dict(PlaceForm.PLACE_TYPES).get(selected_place['place_type']),
            'location': selected_place['location'] or 'Secret place👀',
            'rating': selected_place['rating'],
        })
    
    return render(request, 'random_place.html', {'place': selected_place})
