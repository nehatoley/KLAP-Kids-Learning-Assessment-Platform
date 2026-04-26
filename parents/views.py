from django.http import HttpResponse

def parents_home(request):
    return HttpResponse("Parent App Working")