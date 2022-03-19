from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.hashers import make_password
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, View
from django.contrib.auth import views as auth_views
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from history.models import LoginHistory
from django.core.mail import send_mail
from django.views.generic import View
from django.contrib import messages
from django.conf import settings
from frontend.views import *
from .models import *
from .forms import *
import random as r
import logging

db_logger = logging.getLogger('db')


"""
Admin login
"""


class AdminLoginView(TemplateView):
    try:
        def get(self, request, *args, **kwargs):
            return redirect('accounts:login')
    except Exception as e:
        db_logger.exception(e)

"""
logout view
"""       
class LogOutView(View):
    def get(self,request,*args,**kwargs):
        try:
            logout(request)
            return redirect('accounts:login')
        except Exception as e:
            db_logger.exception(e)


"""
singup view
"""
class SignupView(View):
    def get(self,request,*args,**kwargs):
        return render(request,'registration/signup.html' , {'change' :'signup'})
    
    def post(self,request,*args,**kwargs):
        try:
            email = request.POST.get("email")
            password = request.POST.get("password")
            confirm_password = request.POST.get("password2")
            if not email:
                messages.error(request, 'Please enter email.')
                return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

            if not password:
                messages.error(request, 'Please type password.')
                return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

            if not confirm_password:
                messages.error(request, 'Please type confirm password.')
                return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
            
            if password != confirm_password:
                messages.error(request, 'Your password and confirm password does not match.')
                return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
            
            if User.objects.filter(email=email):
                messages.error(request, 'User already exist with same email.')
                return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
            new=email.split('@')
            username=new[0]
            if User.objects.filter(username=username):
                apndx=""
                for i in range(4):
                    apndx+=str(r.randint(1,9))
                username=str(new[0])+str(apndx)
            user = User.objects.create(email=email,username=username)
            user.set_password(password)
            user.role_id = 2
            user.save()
            messages.success(request, 'Signed up successfully.')
            return redirect('accounts:login')
        except Exception as e:
            db_logger.exception(e)

"""
Login view
"""
class LoginView(View):
    def get(self,request,*args,**kwargs):
        try:
            return render(request,'registration/login.html' , {'change' : "login"})
        except Exception as e:
            db_logger.exception(e)
    
    def post(self,request,*args,**kwargs):
        try:
            agent=request.META['HTTP_USER_AGENT']
            IP=request.META.get("REMOTE_ADDR")
            des= request.path
            urls="http://"+IP+des
            email = request.POST.get("email")
            password = request.POST.get("password")

            if not email:
                feed = LoginHistory.objects.create(User_Ip=IP,User_agent=agent,State="Failed",Code=urls)
                feed.save()
                return render(request, 'registration/login.html',{"email":email})
            
            if not password:
                feed = LoginHistory.objects.create(User_Ip=IP,User_agent=agent,State="Failed",Code=urls,user=email)
                feed.save()
                return render(request, 'registration/login.html',{"email":email})

            if request.POST.get('remember_me')=='on':
                request.session.set_expiry(7600) 
                
            user = authenticate(username=email, password=password)
            if not user:
                feed = LoginHistory.objects.create(User_Ip=IP,User_agent=agent,State="Failed",Code=urls,user=email)
                feed.save()
                messages.error(request, 'Invalid login details.')         
                return render(request, 'registration/login.html',{"email":email})
            
            if user.is_superuser and user.role_id == 1:
                login(request, user)
                feed = LoginHistory.objects.create(User_Ip=IP,User_agent=agent,State="success",Code=urls,user=email)
                feed.save()
                return redirect('admin:index')

            login(request, user)
            feed = LoginHistory.objects.create(User_Ip=IP,User_agent=agent,State="success",Code=urls,user=email)
            feed.save()
            return redirect('frontend:index')
        except Exception as e:
            db_logger.exception(e)


'''
Forgot Password Views
'''

def password_reset_complete(request):
    try:
        response = auth_views.PasswordResetCompleteView.as_view()(request)
        return response
    except Exception as e:
        db_logger.exception(e)

def password_reset_confirm(request, uidb64=None, token=None):
    response = auth_views.PasswordResetConfirmView.as_view()(request,
                                                             uidb64=uidb64,
                                                             token=token,
                                                             post_reset_redirect="/")

    return response


def password_reset_done(request):
    try:
        return render(request,"registration/password_reset_done.html",{})
    except Exception as e:
        db_logger.exception(e)


class ResetPasswordView(auth_views.PasswordResetView):
    form_class = EmailValidationOnForgotPasswordForm

