from django.shortcuts import render
from scraping.models import EuroMillionsResult

# Create your views here.

def index(request):
    """ A view to return the index page """

    return render(request, 'home/index.html')


from django.shortcuts import render
from scraping.models import EuroMillionsResult  # Ensure correct import

def latest_draw(request):
    try:
        latest_result = EuroMillionsResult.objects.latest('id')  # Use 'id' if that's a reliable field
        print("Latest result fetched successfully:", latest_result)  # Debug statement
    except EuroMillionsResult.DoesNotExist:
        latest_result = None
        print("No results found.")  # Debug statement
    
    return render(request, 'home/index.html', {'latest_result': latest_result})

