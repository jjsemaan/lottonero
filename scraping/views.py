from django.shortcuts import render, redirect
from django.core.management import call_command

def run_scrape_euromillions(request):
    # Call the custom command
    call_command('scrape_euromillions')

    # Redirect or render a response after execution
    return redirect('backoffice')  # Redirect to a URL name, or you can render a template

