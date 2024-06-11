from django.shortcuts import render, redirect
from django.core.management import call_command
import io

def run_scrape_euromillions(request):
    # Capture the command output
    out = io.StringIO()
    call_command('scrape_euromillions', stdout=out)
    result = out.getvalue()
    
    # Check the command output for specific messages
    if "have already been scraped" in result:
        return redirect('scraping:backoffice_failed')  # Redirect to the failed URL
    else:
        return redirect('scraping:backoffice_success')  # Redirect to the success URL

def backoffice_success(request):
    return render(request, 'scraping/backoffice_success.html')

def backoffice_failed(request):
    return render(request, 'scraping/backoffice_failed.html')
