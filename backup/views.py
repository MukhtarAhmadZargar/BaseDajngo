import os
import time
import logging
from getpass import getpass
from datetime import datetime
from django.contrib import messages
from django.shortcuts import render ,redirect
from mysql.connector import connect, Error
from django.views.generic import View,TemplateView
from accounts.models import *
from django.http import HttpResponse
from django.utils.encoding import smart_str
from django.http.response import HttpResponse
from .models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
db_logger = logging.getLogger('db')

@login_required
def backup(request):
	try:
		data_table = backups.objects.all().order_by('-id')
		return render(request, "backup/backup.html",{"data":data_table})
	except Exception as e:
		db_logger.exception(e)

@login_required
def database_backup(request):
	try:
		username = 'admin'
		password = 'admin@123'
		database = 'python-base'
		BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
		path= os.path.join(BASE_DIR)
		BACKUP_PATH = f'{path}/backup/backups/sql_files/'
		DATETIME = time.strftime('%Y%m%d-%H%M%S')
		TODAYBACKUPPATH = BACKUP_PATH + '/' + DATETIME
		dumpcmd = "mysqldump -h " + "localhost" + " -u " + username + " -p" + password + " " + database + " > " + BACKUP_PATH + "/" + database+DATETIME + ".sql"
		os.system(dumpcmd)
		name= database+DATETIME + ".sql"
		size = os.path.getsize(f"{path}/backup/backups/sql_files/"+name)
		
		value=backups.objects.create(Name=name,Size=size,create_on=datetime.now(), 
							create_at=datetime.now(), create_by=request.user.username)
		messages.success(request, "Backup Created Successfully")
		data_table = backups.objects.all().values()
		return redirect('backup:backup')

	except Exception as e:
		db_logger.exception(e)

@login_required
def downloadDbFile(request):
	try:
		if request.method == 'GET':
			BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
			path= os.path.join(BASE_DIR)
			backup = backups.objects.get(id=request.GET.get("id"))
			file_name = backup.Name
			file_path = f"{path}/backup/backups/sql_files/{file_name}"
			filepath= file_path
			with open(filepath, 'r') as f:
				response = HttpResponse(f.read(), content_type='application/sql')
				response['Content-Disposition'] = 'inline; filename=' + file_name
				return response
	except Exception as e:
		db_logger.exception(e)

@login_required
def downloadFile(request):
	try:
		BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
		path= os.path.join(BASE_DIR)
		backup = backups.objects.get(id=request.GET.get("id"))
		file_name = backup.Name

		file_path = f"{path}/backup/backups/sql_files/{file_name}"
		filepath= file_path
		with open(filepath, 'r') as f:
				response = HttpResponse(f.read(), content_type='application/sql')
				response['Content-Disposition'] = 'inline; filename=' + file_name
		return response
	except Exception as e:
		db_logger.exception(e)

@login_required
def DeleteBackup(request):
	try:
		if request.method == 'GET':
			backup = backups.objects.get(id=request.GET.get("id"))
			if backup:
				messages.success(request, "Backup Deleted Successfully")
				backup.delete()
			return redirect('backup:backup')
	except Exception as e:
		db_logger.exception(e)