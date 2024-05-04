from django.shortcuts import render
from scraping.models import EuroMillionsResult

# Create your views here.

def index(request):
    """ A view to return the index page """

    return render(request, 'home/index.html')


def latest_draw(request):
    latest_result = EuroMillionsResult.objects.latest('id')  # Assuming 'id' or you can also use 'draw_date'
    context = {
        'latest_result': latest_result,
    }
    return render(request, 'home/index.html', context)
