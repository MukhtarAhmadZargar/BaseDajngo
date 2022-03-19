
from django.shortcuts import render,redirect
from accounts.models import User 
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from accounts.models import Activities
from django.http import HttpResponse
import os
"""
Index Page
"""
def index(request):
        if request.user.is_authenticated == True and request.user.is_superuser and request.user.role_id == 1:
            return redirect('admin:index')
        else:
            return render(request, "frontend/index.html", {'status' : 'home'})


def robot(request):
	BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	path= os.path.join(BASE_DIR)
	fin = open(f'{path}/project/robots.txt', 'rb')
	file_content = fin.read()
	fin.close()
	return HttpResponse(file_content, content_type="text/plain")



"""
error pages
"""
def error_404(request, exception):
    data = {}
    return render(request,'frontend/404.html', data)
    
def error_500(request):
    data = {}
    return render(request,'frontend/404.html', data)

