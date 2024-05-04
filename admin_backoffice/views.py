from django.shortcuts import render


from django.shortcuts import render

def backoffice_home(request):
    return render(request, 'admin_backoffice/backoffice.html')
