from django.shortcuts import render
from scraping.models import EuroMillionsResult

# Create your views here.

def index(request):
    """ A view to return the index page """

    return render(request, 'home/index.html')


def latest_draw(request):
    """ A view to return the last draw results from the db """
    latest_result = EuroMillionsResult.objects.latest('id')
    context = {
        'latest_result': latest_result,
    }
    return render(request, 'home/index.html', context)
