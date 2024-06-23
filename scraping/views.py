from django.shortcuts import render
from django.core.management import call_command
from django.contrib import messages
import io

def run_scrape_euromillions(request):
    """
    Executes the 'scrape_euromillions' management command and displays feedback messages directly on the backoffice dashboard.

    This function runs the scraping command and uses Django's messaging framework to provide immediate feedback based on the
    command's output, displaying messages on the backoffice dashboard located within the 'predictions' app.

    Args:
        request (HttpRequest): The HttpRequest object containing metadata about the request.

    Returns:
        HttpResponse: Renders the 'backoffice/backoffice.html' template displaying success or error messages.
    """
    out = io.StringIO()
    call_command('scrape_euromillions', stdout=out)
    result = out.getvalue()
    
    if "have already been scraped" in result:
        messages.error(request, "No new data to scrape. All available data have already been scraped.")
    else:
        messages.success(request, "Data scraped successfully.")

    return render(request, 'backoffice/backoffice.html')

def backoffice(request):
    """
    Renders the backoffice dashboard for the predictions app where administrative actions like scraping can be initiated.

    This view serves as a central dashboard within the 'predictions' app where users can manage scraping tasks and view the results
    through messages displayed on the same page.
    """
    return render(request, 'backoffice/backoffice.html')