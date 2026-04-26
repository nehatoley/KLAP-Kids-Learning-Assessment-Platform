from django.http import HttpResponse

def teacher_home(request):
    return HttpResponse("Teacher Working")