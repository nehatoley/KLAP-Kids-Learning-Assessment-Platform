from django.http import HttpResponse

def admin_home(request):
    return HttpResponse("Admin Dashboard Working")