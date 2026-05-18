from django.http import HttpRequest, HttpResponse



# Create your views here.
def hello(request):
    return HttpResponse("Hello, Oleg!")