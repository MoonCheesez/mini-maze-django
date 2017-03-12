from django.shortcuts import render

# Create your views here.
def screen(request):
	return render(request, 'screen/screen.html', {})