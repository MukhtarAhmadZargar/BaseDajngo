from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate,login
from django.shortcuts import render, redirect
from accounts.models import User,Activities
from django.views.generic import View
from django.contrib import messages
from contact.models import Contact
from tablib import Dataset
import pandas as pd
import logging
import time
import csv
import os


db_logger = logging.getLogger('db')


"""
AllUser
"""
@login_required
def Allusers(request):
    try:
        users=User.objects.all().order_by("-id").exclude(role_id=1)
        page = request.GET.get('page', 1)
        paginator = Paginator(users, 7)
        try:
            users = paginator.page(page)
        except PageNotAnInteger:
            users = paginator.page(1)
        except EmptyPage:
            users = paginator.page(paginator.num_pages)
        return render(request,'admin/users/users.html', {"users":users} )
    except Exception as e:
        db_logger.exception(e)


"""
Add View
"""

class AddUser(View):
    @method_decorator(login_required)
    def get(self,request,*args,**kwargs):
        return render(request, 'admin/users/add-user.html')
    def post(self,request,*args,**kwargs):
        try:
            user={
                    'username':request.POST.get("username"),
                    'fullname':request.POST.get('fullname'),
                    'email': request.POST.get('email'),
                }
            if User.objects.filter(email=request.POST.get('email')):
                    messages.error(request, 'User already exist with same email.')
                    return render(request, 'admin/users/add-user.html',{"user":user})

            if User.objects.filter(username=request.POST.get('username')):
                    messages.error(request, 'User already exist with same username.')
                    return render(request, 'admin/users/add-user.html',{"user":user})

            if User.objects.filter(username=request.POST.get('email')):
                messages.error(request, 'please enter another email.')
                return render(request, 'admin/users/add-user.html',{"user":user})

            if User.objects.filter(email=request.POST.get('username')):
                messages.error(request, 'please enter another username.')
                return render(request, 'admin/users/add-user.html',{"user":user})
            
            password=request.POST.get('password')
            try:
                pic=request.FILES.get('profile_pic')
                if pic:
                    ext = os.path.splitext(pic.name)[1]
                    valid_extensions = ['.tif', '.tiff', '.bmp', '.jpg', '.JPG','.jpeg', '.JPEG','.gif','.png','.PNG']
                    if not ext.lower() in valid_extensions:
                        messages.error(request, 'Unsupported File Format. please select proper Image Format')
                        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
            except:
                pic=""
                
            User.objects.create(full_name =request.POST.get('fullname'),username=request.POST.get('username'),
                                        email=request.POST.get('email'),password=make_password(password),
                                        role_id=2, profile_pic=pic)
            messages.success(request, 'User added successfully')
            return redirect('Admin:allusers')
        except Exception as e:
            db_logger.exception(e)


'''
Profile View
'''
@login_required
def ViewUser(request,id):
    try:
        user=User.objects.get(id=id)
        return render(request, 'admin/profile.html', {'user':user})
    except Exception as e:
        db_logger.exception(e)


'''
Edit User
'''
class EditUser(View):
    @method_decorator(login_required)
    def get(self,request,*args,**kwargs):
        try:
            user=User.objects.get(id=request.GET.get("id"))
            return render(request, 'admin/users/edit-user.html',{"user":user})
        except Exception as e:
            db_logger.exception(e)

    def post(self,request,*args,**kwargs):
        try:
            user=User.objects.get(id=request.GET.get("id"))

            if request.POST.get("username"):
                username=request.POST.get("username")
                if User.objects.filter(username=username).exclude(id=user.id):
                    messages.error(request, 'Other User already exist with same username.')
                    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
                user.username = username

            if User.objects.filter(email=request.POST.get('username')):
                messages.error(request, 'please enter another username.')
                return render(request, 'admin/users/edit-user.html',{"user":user})


            if request.POST.get("address"):
                user.address = request.POST.get("address")

            if request.FILES.get("profile_pic"):
                ext = os.path.splitext(request.FILES.get("profile_pic").name)[1]
                valid_extensions = ['.jpg', '.png', '.JPEG', '.jpeg']
                if not ext.lower() in valid_extensions:
                    messages.error(request, 'Unsupported FIle Format.')
                    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
                user.profile_pic= request.FILES.get("profile_pic")

            
            user.save()
            messages.success(request, 'User Edited successfully')
            return redirect('Admin  :View_User', id=user.id)
        except Exception as e:
            db_logger.exception(e)

'''
Delete User
'''

@login_required
def DeleteUser(request):
    try:
        id = request.GET.get('id')
        user=User.objects.get(id =id)
        if user:
            Activities.objects.create(performed_by=request.user, user_id= user.id, performed_for=user.username, action_taken="Deleted")
            user.state_id = 3
            user.is_active = False
            messages.success(request, 'user Deleted ')
        user.save()
        return redirect('Admin:allusers')
    except Exception as e:
        db_logger.exception(e)


'''
Delete User
'''

@login_required
def DeleteUserindex(request):
    try:
        id = request.GET.get('id')
        user=User.objects.get(id =id)
        if user:
            Activities.objects.create(performed_by=request.user, user_id= user.id, performed_for=user.username, action_taken="Deleted")
            user.state_id = 3
            user.is_active = False
            messages.success(request, 'user Deleted ')
        user.save()
        return redirect('frontend:index')
    except Exception as e:
        db_logger.exception(e)  


"""
Change State of User
"""

def ChangeStatusDelete(request):
    user = User.objects.get(id=request.GET.get("id"))
    if user:
        user.state_id = 3
        user.is_active = False
        user.save()
    return render(request, 'admin/profile.html' , {"user":user})


@login_required
def ChangeStatusActive(request):
    user = User.objects.get(id=request.GET.get("id"))
    if user:
        user.state_id = 1
        user.is_active = True
        user.save()
    return render(request, 'admin/profile.html' , {"user":user})

@login_required
def ChangeStatusInactive(request):
    user = User.objects.get(id=request.GET.get("id"))
    if user:
        user.state_id = 2
        user.is_active = False
        user.save()
    return render(request, 'admin/profile.html' , {"user":user})




"""
change password
"""
class PasswordChange(View):
    @method_decorator(login_required)
    def get(self,request,*args,**kwargs):
        return render(request,'admin/change-password.html')

    def post(self,request,*args,**kwargs):
        id=request.user.id
        user=User.objects.get(id=id)
        pass1 = request.POST.get("password")
        match= check_password(pass1, user.password)
        if match:
            messages.error(request, 'Choose A different Passsword ')
            return render(request,'admin/change-password.html')
        else:
            user.set_password(pass1)
            user.save()
            messages.add_message(request, messages.INFO, 'Password changed successfully')
            return redirect('accounts:login')



"""
Download and upload CSV views
"""
@login_required
def Download_CSV(request):
    try:
        DATETIME = time.strftime('%Y%m%d-%H%M%S')
        name= "BaseProject" + DATETIME
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename= '+ name +".csv"
        writer = csv.writer(response)
        writer.writerow(['User ID','FullName','Email','Username'])
        users = User.objects.all().exclude(role_id=1).values_list('id','full_name','email','username')

        if not users:
            messages.error(request, 'Not enough Users , to get CSV')
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

        for user in users:
            writer.writerow(user)
        return response
    except Exception as e:
        db_logger.exception(e)


@login_required
def UploadCSV(request):
    try:
        if request.method =="POST":
            filename = request.FILES.get('file')
            ext = os.path.splitext(filename.name)[1]
            valid_extensions = ['.csv', '.CSV', '.xls', '.xlsx']
            validformat=['Fullname', 'Email', 'Username', 'Password']
            if not ext.lower() in valid_extensions:
                messages.error(request, 'Unsupported FIle Format.')
                return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
            try:
                excel_ext=[ '.xls', '.xlsx']
                if ext.lower() in excel_ext:
                    dataset = Dataset()
                    imported_data = dataset.load(filename.read(),format='xlsx')
                    if imported_data.headers==validformat:
                        for data in imported_data:
                            if len(data)==4:
                                Fullname =str(data[0])
                                Email = str(data[1])
                                Username = str(data[2])
                                Password = str(data[3])
                            else:
                                messages.error(request, "Some Columns Missing!  it  should be: Fullname, Email, Username, Password" )
                                return redirect('Admin:allusers')

                            if User.objects.filter(username=Username):
                                messages.error(request, "Username in file , already Exist in Database" )
                                return redirect('Admin:allusers')

                            if User.objects.filter(email=Email):
                                messages.error(request, "Email in file , already Exist in Database" )
                                return redirect('Admin:allusers')
                            
                            user=User.objects.create(username=Username,email=Email, full_name=Fullname, role_id = 2 , password=make_password(Password))
                            user.save()
                        messages.success(request,"Created Successfully!!..")
                        return redirect('Admin:allusers')
                    messages.error(request, "Format  should be: Fullname, Email, Username, Password" )
                    return redirect('Admin:allusers')
                else:
                    data = pd.read_csv (filename)
                    df = pd.DataFrame(data)  
                    df =df[['FullName','Email','Username','Password']]     
                    row = df.iterrows()
                    length=len(df)
                    for i in range(1,length+1):
                        new=next(row)[1]
                        if len(new)==4:
                            Fullname = new[0]
                            Email = new[1]
                            Username = new[2]
                            Password = new[3]
                        else:
                            messages.error(request, "Some Columns Missing!  it  should be: Fullname, Email, Username, Password" )
                            return redirect('Admin:allusers')

                        if User.objects.filter(username=Username):
                            messages.error(request, "Username in file , already Exist in Database" )
                            return redirect('Admin:allusers')

                        if User.objects.filter(email=Email):
                            messages.error(request, "Email in file , already Exist in Database" )
                            return redirect('Admin:allusers')

                        user=User.objects.create(username=Username,email=Email, full_name=Fullname, role_id = 2 , password=make_password(Password))
                        user.save()
                        messages.success(request,"Created Successfully!!..")
                        return redirect('Admin:allusers')
                messages.error(request, "Format  should be: Fullname, Email, Username, Password" )
                return redirect('Admin:allusers')
            except:
                messages.error(request, "Format  should be: Fullname, Email, Username, Password" )
        return redirect('Admin:allusers')
    except Exception as e:
        db_logger.exception(e)
