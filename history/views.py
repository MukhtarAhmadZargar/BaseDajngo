from django.contrib import messages
from django.shortcuts import render,redirect
from .models import LoginHistory
from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required
def LoginHistoryView(request):
    return render(request, 'login-history/login-history.html')


@login_required
def DeleteHistory(request):
    history=LoginHistory.objects.all()
    if history:
        history.delete()
        messages.success(request,"All Login History Cleared Sucessfully!!!")
    else:
        messages.error(request,"Nothing to Delete!!!")
    return redirect('history:login_history')