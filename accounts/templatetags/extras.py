from django.db.models.functions import ExtractMonth
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta
from django.db.models import Sum, Count
from django.http import JsonResponse
from django.db.models import Count
from django.utils import timezone
from django.db.models import Sum
from datetime import datetime
from accounts.models import *
from blog.models import Blog
from contact.models import *
from history.models import *
from django import template




register = template.Library()

last_month = datetime.today() - timedelta(days=1)

@register.filter(name='total_users')
def total_users(key):
	return User.objects.all().count()


@register.filter(name='users')
def users(key):
	return User.objects.all().exclude(role_id=1).order_by('-id')


@register.filter(name='total_contacts')
def total_contacts(key):
	contacts = Contact.objects.all().count()
	return contacts

@register.filter(name='login_history')
def login_history(key):
	user = LoginHistory.objects.all().order_by('-id')
	return user


@register.filter(name='total_login_history')
def total_login_history(key):
	user = LoginHistory.objects.all().count()
	return user
	
@register.filter(name='total_blogs')
def total_blogs(key):
	blogs = Blog.objects.all().count()
	return blogs

@register.filter(name='Usergraph')
def Usergraph(key):
    user = []
    months = {'jan':'1','feb':'2','mar':'3','apr':'4','may':'5','jun':'6','jul':'7','aug':'8','sep':'9','oct':'10','nov':'11','dec':'12'}
    for i in months.keys():
        x = User.objects.filter(created_on__year=str(datetime.now().year),created_on__month= months[i]).annotate(count=Count('id')).count()
        user.append(x)

        chart = {
			'chart': {'type': 'spline'},
			'title': {'text': 'Monthly'},
			'xAxis': { 'categories': [i.upper() for i in months.keys()]},
			'colors': ['#2bc155'],
			'series': [{
				'name': 'Health Records',
				'data':user
				}]
			}
        return user
