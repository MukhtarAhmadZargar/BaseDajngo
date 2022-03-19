import logging
from django.shortcuts import render
from django_db_logger.models import StatusLog
# Create your views here.


db_logger = logging.getLogger('db')

def Loggs(request):
    logs=StatusLog.objects.all()
    return render(request, 'dblogger/logs.html', { 'logs':logs })


def LogView(request):
    id=request.GET.get('id')
    log=StatusLog.objects.get(id=id)
    return render(request, 'dblogger/view-log.html', {'log':log})